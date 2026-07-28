from pathlib import Path

from pocket_agent.config.models import PathsConfig
from pocket_agent.indexing.scanner import build_file_index, get_index_store
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.files.paths import is_under_allowed_root


async def list_nas_files(
    paths: PathsConfig,
    location: str | None = None,
    limit: int = 50,
) -> ToolResult:
    """List files under NAS allowed roots."""
    root = Path(location).expanduser() if location else paths.nas_root

    if not is_under_allowed_root(root, paths.allowed_read_roots):
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


async def index_files(paths: PathsConfig, max_depth: int | None = None) -> ToolResult:
    """Scan NAS roots and rebuild the SQLite file index."""
    depth = max_depth if max_depth is not None else paths.index_max_depth
    exclude = paths.index_exclude_dirs or None
    try:
        _, count = await build_file_index(
            paths,
            exclude_dir_names=exclude,
            max_depth=depth,
        )
        return ToolResult(
            success=True,
            data={"indexed_count": count, "db_path": str(paths.index_db_path)},
        )
    except OSError as exc:
        log_action(
            paths.logs_dir,
            "index_files",
            {},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))


async def search_files(
    paths: PathsConfig,
    query: str,
    location: str | None = None,
    extension: str | None = None,
    limit: int = 25,
) -> ToolResult:
    """Search indexed files; falls back to filesystem walk if index is empty."""
    store = get_index_store(paths)
    index_count = store.count()

    if index_count > 0:
        records = store.search(query=query, extension=extension, limit=limit)
        if location:
            location_resolved = str(Path(location).expanduser().resolve())
            records = [r for r in records if r.path.startswith(location_resolved)]

        matches = [
            {
                "path": r.path,
                "name": r.name,
                "extension": r.extension,
                "size_bytes": str(r.size_bytes),
            }
            for r in records
        ]
        log_action(
            paths.logs_dir,
            "search_files",
            {"query": query, "source": "index", "count": len(matches)},
        )
        return ToolResult(
            success=True,
            data={"matches": matches, "query": query, "source": "index"},
        )

    root = Path(location).expanduser() if location else paths.nas_root
    if not is_under_allowed_root(root, paths.allowed_read_roots):
        return ToolResult(success=False, error=f"Path not allowed: {root}")

    if not root.exists():
        return ToolResult(success=False, error=f"NAS path not found: {root}")

    query_lower = query.lower()
    ext_filter = extension.lower().lstrip(".") if extension else None
    matches: list[dict[str, str]] = []

    try:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if ext_filter and path.suffix.lower().lstrip(".") != ext_filter:
                continue
            if query_lower in path.name.lower() or query_lower in str(path).lower():
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
        {"query": query, "location": str(root), "count": len(matches), "source": "filesystem"},
    )
    return ToolResult(
        success=True,
        data={"matches": matches, "query": query, "source": "filesystem"},
    )
