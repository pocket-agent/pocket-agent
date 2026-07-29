import hashlib
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult

Validator = Callable[[Path], tuple[bool, str]]


@dataclass
class SafeEditSession:
    original_path: Path
    backup_path: Path
    working_path: Path
    original_checksum: str
    original_size: int


def file_checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def prepare_safe_edit(
    paths: PathsConfig,
    original_path: Path,
    tool_name: str,
) -> SafeEditSession | ToolResult:
    paths.backup_dir.mkdir(parents=True, exist_ok=True)
    paths.working_dir.mkdir(parents=True, exist_ok=True)

    if not original_path.is_file():
        return ToolResult(success=False, error=f"File not found: {original_path}")

    original_size = original_path.stat().st_size
    if original_size == 0:
        return ToolResult(success=False, error="Refusing to edit empty file")

    max_bytes = 50 * 1024 * 1024
    if original_size > max_bytes:
        return ToolResult(success=False, error="File exceeds 50MB edit limit")

    stamp = _timestamp()
    backup_name = f"{original_path.stem}_{stamp}{original_path.suffix}"
    backup_path = paths.backup_dir / backup_name
    working_name = f"{stamp}_{original_path.name}"
    working_path = paths.working_dir / working_name

    try:
        shutil.copy2(original_path, backup_path)
        shutil.copy2(original_path, working_path)
    except OSError as exc:
        log_action(
            paths.logs_dir,
            tool_name,
            {"original": str(original_path)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=f"Backup failed: {exc}")

    session = SafeEditSession(
        original_path=original_path.resolve(),
        backup_path=backup_path.resolve(),
        working_path=working_path.resolve(),
        original_checksum=file_checksum(original_path),
        original_size=original_size,
    )

    log_action(
        paths.logs_dir,
        f"{tool_name}_prepare",
        {
            "original": str(session.original_path),
            "backup": str(session.backup_path),
            "working": str(session.working_path),
        },
    )
    return session


def finalize_safe_edit(
    paths: PathsConfig,
    session: SafeEditSession,
    validator: Validator,
    tool_name: str,
    require_change: bool = True,
) -> ToolResult:
    working = session.working_path

    if not working.is_file():
        return ToolResult(success=False, error="Working copy missing after edit")

    new_size = working.stat().st_size
    if new_size == 0:
        return ToolResult(success=False, error="Validation failed: working copy is empty")

    if new_size > session.original_size * 10 and new_size > 50 * 1024 * 1024:
        return ToolResult(success=False, error="Validation failed: output size suspicious")

    ok, reason = validator(working)
    if not ok:
        log_action(
            paths.logs_dir,
            f"{tool_name}_validate",
            {"working": str(working)},
            success=False,
            error=reason,
        )
        return ToolResult(success=False, error=f"Validation failed: {reason}")

    new_checksum = file_checksum(working)
    if require_change and new_checksum == session.original_checksum:
        return ToolResult(success=False, error="Validation failed: no changes detected")

    try:
        shutil.copy2(working, session.original_path)
    except OSError as exc:
        log_action(
            paths.logs_dir,
            f"{tool_name}_replace",
            {"original": str(session.original_path)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=f"Replace failed: {exc}")

    log_action(
        paths.logs_dir,
        f"{tool_name}_complete",
        {
            "original": str(session.original_path),
            "backup": str(session.backup_path),
            "working": str(session.working_path),
            "new_size": new_size,
        },
    )

    return ToolResult(
        success=True,
        data={
            "path": str(session.original_path),
            "backup_path": str(session.backup_path),
            "working_path": str(session.working_path),
            "original_size": session.original_size,
            "new_size": new_size,
        },
    )


def rollback_from_backup(session: SafeEditSession, paths: PathsConfig, tool_name: str) -> ToolResult:
    try:
        shutil.copy2(session.backup_path, session.original_path)
        log_action(
            paths.logs_dir,
            f"{tool_name}_rollback",
            {"original": str(session.original_path), "backup": str(session.backup_path)},
        )
        return ToolResult(success=True, data={"restored_from": str(session.backup_path)})
    except OSError as exc:
        return ToolResult(success=False, error=str(exc))
