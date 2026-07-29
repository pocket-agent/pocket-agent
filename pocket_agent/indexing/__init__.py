"""File indexing and search over SQLite."""

from pocket_agent.indexing.scanner import build_file_index, get_index_store, scan_roots
from pocket_agent.indexing.store import FileIndexStore

__all__ = ["FileIndexStore", "build_file_index", "get_index_store", "scan_roots"]
