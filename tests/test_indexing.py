from pathlib import Path

import pytest

from pocket_agent.config.models import PathsConfig
from pocket_agent.indexing.scanner import build_file_index, scan_roots
from pocket_agent.indexing.store import FileIndexStore


def _paths(tmp_path: Path) -> PathsConfig:
    nas = tmp_path / "nas"
    nas.mkdir()
    (nas / "invoice.pdf").write_bytes(b"%PDF-1.4")
    (nas / "notes.txt").write_text("hello notes")
    sub = nas / "tax"
    sub.mkdir()
    (sub / "tax-2024.pdf").write_bytes(b"%PDF-1.4")

    return PathsConfig(
        {
            "nas": {"root": str(nas), "allowed_read_roots": [str(nas)]},
            "data": {"logs": "data/logs", "cache": "data/cache"},
            "index": {"db_path": "data/cache/file_index.db"},
        },
        tmp_path,
    )


def test_scan_roots(tmp_path: Path):
    paths = _paths(tmp_path)
    records = scan_roots(paths)
    assert len(records) >= 3


@pytest.mark.asyncio
async def test_build_file_index(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    store, count = await build_file_index(paths)
    assert count >= 3
    assert store.count() == count


def test_index_search(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    records = scan_roots(paths)
    store = FileIndexStore(paths.index_db_path)
    store.clear()
    store.upsert_batch(records, indexed_at=1.0)

    results = store.search("tax")
    assert any("tax" in r.name.lower() for r in results)
