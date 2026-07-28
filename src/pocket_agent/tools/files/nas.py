from pathlib import Path

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult


def _is_under_allowed_root(path: Path, allowed_roots: list[Path]) -> bool:
    resolved = path.resolve()
    for root in allowed_roots:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


async def list_nas_files(
    paths: PathsConfig,
    location: str | None = None,
    limit: int = 50,
) -> ToolResult:
    """List files under NAS allowed roots. See TOOLS_SPEC search_files (Phase 2)."""
    root = Path(location).expanduser() if location else paths.nas_root

    if not _is_under_allowed_root(root, paths.allowed_read_roots):
        log_action(
            paths.logs_dir,
            "list_nas_files",
            {"location": str(root)},
            success=False,
            error="path not in allowed_read_roots",
        )
        return ToolResult(success=False, error=f"Path not allowed: {root}")

    if not root.exists():
        log_action(
            paths.logs_dir,
            "list_nas_files",
            {"location": str(root)},
            success=False,
            error="path does not exist",
        )
        return ToolResult(success=False, error=f"NAS path not found: {root}")

    entries: list[dict[str, str]] = []
    try:
        for item in sorted(root.iterdir())[:limit]:
            if item.is_file():
                entries.append(
                    {
                        "path": str(item),
                        "name": item.name,
                        "size_bytes": str(item.stat().st_size),
                    }
                )
    except OSError as exc:
        log_action(
            paths.logs_dir,
            "list_nas_files",
            {"location": str(root)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))

    log_action(
        paths.logs_dir,
        "list_nas_files",
        {"location": str(root), "count": len(entries)},
    )
    return ToolResult(success=True, data={"files": entries, "root": str(root)})


async def search_files(
    paths: PathsConfig,
    query: str,
    location: str | None = None,
    limit: int = 25,
) -> ToolResult:
    """Search file names under NAS roots (basename match). Full index in Phase 2."""
    root = Path(location).expanduser() if location else paths.nas_root

    if not _is_under_allowed_root(root, paths.allowed_read_roots):
        return ToolResult(success=False, error=f"Path not allowed: {root}")

    if not root.exists():
        return ToolResult(success=False, error=f"NAS path not found: {root}")

    query_lower = query.lower()
    matches: list[dict[str, str]] = []

    try:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if query_lower in path.name.lower():
                matches.append({"path": str(path), "name": path.name})
            if len(matches) >= limit:
                break
    except OSError as exc:
        log_action(
            paths.logs_dir,
            "search_files",
            {"query": query, "location": str(root)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))

    log_action(
        paths.logs_dir,
        "search_files",
        {"query": query, "location": str(root), "count": len(matches)},
    )
    return ToolResult(success=True, data={"matches": matches, "query": query})
