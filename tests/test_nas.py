from pathlib import Path

import pytest

from pocket_agent.config.models import PathsConfig
from pocket_agent.tools.files.nas import list_nas_files, search_files


def _paths(tmp_path: Path) -> PathsConfig:
    nas = tmp_path / "nas"
    nas.mkdir()
    (nas / "invoice.pdf").write_text("x")
    (nas / "notes.txt").write_text("y")
    sub = nas / "tax"
    sub.mkdir()
    (sub / "tax-2024.pdf").write_text("z")

    return PathsConfig(
        {
            "nas": {
                "root": str(nas),
                "allowed_read_roots": [str(nas)],
            },
            "data": {"logs": "data/logs"},
        },
        tmp_path,
    )


@pytest.mark.asyncio
async def test_list_nas_files(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    result = await list_nas_files(paths)
    assert result.success
    assert len(result.data["files"]) >= 2


@pytest.mark.asyncio
async def test_search_files(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    result = await search_files(paths, query="tax")
    assert result.success
    assert any("tax" in m["name"].lower() for m in result.data["matches"])


@pytest.mark.asyncio
async def test_rejects_disallowed_path(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    result = await list_nas_files(paths, location=str(outside))
    assert not result.success
