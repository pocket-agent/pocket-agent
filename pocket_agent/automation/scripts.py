"""Run allowlisted maintenance scripts."""

from __future__ import annotations

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Any

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)


def _resolve_allowed(project_root: Path, raw_settings: dict[str, Any]) -> dict[str, Path]:
    automation = raw_settings.get("automation", {})
    entries = automation.get("allowed_scripts", [])
    allowed: dict[str, Path] = {}
    if not isinstance(entries, list):
        return allowed

    for item in entries:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        rel = str(item.get("path", "")).strip()
        if not name or not rel:
            continue
        path = Path(rel)
        if not path.is_absolute():
            path = (project_root / rel).resolve()
        allowed[name] = path
    return allowed


async def run_allowed_script(
    project_root: Path,
    raw_settings: dict[str, Any],
    script_name: str,
    timeout_seconds: int = 120,
) -> ToolResult:
    name = (script_name or "").strip()
    if not name:
        return ToolResult(success=False, error="script_name is required")

    allowed = _resolve_allowed(project_root, raw_settings)
    path = allowed.get(name)
    if path is None:
        return ToolResult(
            success=False,
            error=f"Script '{name}' is not allowlisted in config automation.allowed_scripts",
        )
    if not path.is_file():
        return ToolResult(success=False, error=f"Script file not found: {path}")

    timeout = max(10, min(int(timeout_seconds), 600))

    try:
        proc = await asyncio.to_thread(
            subprocess.run,
            [str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(project_root),
        )
        stdout = (proc.stdout or "")[:4000]
        stderr = (proc.stderr or "")[:2000]
        ok = proc.returncode == 0
        return ToolResult(
            success=ok,
            data={
                "script": name,
                "path": str(path),
                "exit_code": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
            },
            error=None if ok else f"exit code {proc.returncode}",
        )
    except subprocess.TimeoutExpired:
        return ToolResult(success=False, error=f"Script timed out after {timeout}s")
    except Exception as exc:
        logger.exception("run_allowed_script failed")
        return ToolResult(success=False, error=str(exc))
