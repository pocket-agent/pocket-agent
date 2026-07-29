import time
from pathlib import Path

from pocket_agent.config.models import PathsConfig
from pocket_agent.indexing.models import FileRecord
from pocket_agent.indexing.store import FileIndexStore
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.files.paths import is_under_allowed_root


def _should_skip_dir(name: str, exclude_names: set[str]) -> bool:
    return name.startswith(".") or name in exclude_names


def scan_roots(
    paths: PathsConfig,
    exclude_dir_names: set[str] | None = None,
    max_depth: int = 12,
) -> list[FileRecord]:
    exclude = exclude_dir_names or {".git", ".Trash", "__pycache__"}
    records: list[FileRecord] = []

    for root in paths.allowed_read_roots:
        if not root.exists():
            continue
        _walk(root, root, records, exclude, max_depth, 0)

    return records


def _walk(
    root: Path,
    current: Path,
    records: list[FileRecord],
    exclude_names: set[str],
    max_depth: int,
    depth: int,
) -> None:
    if depth > max_depth:
        return

    try:
        entries = list(current.iterdir())
    except OSError:
        return

    for entry in entries:
        if entry.is_dir():
            if _should_skip_dir(entry.name, exclude_names):
                continue
            _walk(root, entry, records, exclude_names, max_depth, depth + 1)
        elif entry.is_file():
            stat = entry.stat()
            records.append(
                FileRecord(
                    path=str(entry.resolve()),
                    name=entry.name,
                    extension=entry.suffix.lower().lstrip("."),
                    size_bytes=stat.st_size,
                    modified_at=stat.st_mtime,
                    parent=str(entry.parent),
                )
            )


async def build_file_index(
    paths: PathsConfig,
    exclude_dir_names: set[str] | None = None,
    max_depth: int = 12,
) -> tuple[FileIndexStore, int]:
    store = FileIndexStore(paths.index_db_path)
    records = scan_roots(paths, exclude_dir_names=exclude_dir_names, max_depth=max_depth)
    indexed_at = time.time()
    store.clear()
    if records:
        store.upsert_batch(records, indexed_at=indexed_at)
    log_action(
        paths.logs_dir,
        "build_file_index",
        {"count": len(records), "db": str(paths.index_db_path)},
    )
    return store, len(records)


def get_index_store(paths: PathsConfig) -> FileIndexStore:
    return FileIndexStore(paths.index_db_path)
