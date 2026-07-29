from pathlib import Path

from pocket_agent.config.models import PathsConfig
from pocket_agent.tools.base import ToolResult


def is_under_allowed_root(path: Path, allowed_roots: list[Path]) -> bool:
    resolved = path.resolve()
    for root in allowed_roots:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def resolve_read_path(
    paths: PathsConfig,
    file_path: str,
) -> ToolResult | Path:
    path = Path(file_path).expanduser()
    if not path.is_absolute() and paths.nas_root:
        candidate = paths.nas_root / path
        if candidate.exists():
            path = candidate

    if not is_under_allowed_root(path, paths.allowed_read_roots):
        return ToolResult(success=False, error=f"Path not allowed: {path}")

    if not path.is_file():
        return ToolResult(success=False, error=f"File not found: {path}")

    return path
