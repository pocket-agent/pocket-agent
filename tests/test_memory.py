from pathlib import Path

import pytest

from pocket_agent.config.models import AppSettings, PathsConfig
from pocket_agent.memory.db import MemoryDatabase, looks_like_secret
from pocket_agent.memory.knowledge import KnowledgeBase, chunk_text
from pocket_agent.memory.service import MemoryService
from pocket_agent.memory.skill_retrieval import retrieve_skills
from pocket_agent.core.skill_loader import Skill


def _paths(tmp_path: Path) -> PathsConfig:
    return PathsConfig(
        {
            "data": {"logs": "data/logs", "cache": "data/cache"},
            "memory": {"db_path": "data/cache/memory.db", "chunk_size": 100},
        },
        tmp_path,
    )


def test_chunk_text():
    chunks = chunk_text("abcdefghij", 4)
    assert chunks == ["abcd", "efgh", "ij"]


def test_rejects_secrets():
    assert looks_like_secret("my password=abc")
    assert not looks_like_secret("I like morning summaries")


@pytest.mark.asyncio
async def test_remember_and_recall_fts(tmp_path: Path):
    paths = _paths(tmp_path)
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    env = AppSettings()
    memory = MemoryService(paths, env)

    result = await memory.remember(42, "I prefer Excel reports on Mondays", category="preference")
    assert not isinstance(result, str)

    recalled = await memory.recall("Excel reports", user_id=42, limit=5)
    assert any("Excel" in m.content for m in recalled)


def test_knowledge_base_fts(tmp_path: Path):
    db = MemoryDatabase(tmp_path / "mem.db")
    kb = KnowledgeBase(db, chunk_size=50)
    kb.add_document("/nas/notes.txt", "Company policy on remote work and holidays")
    hits = kb.search_fts("remote work", limit=3)
    assert len(hits) == 1
    assert "remote" in hits[0].text.lower()


def test_skill_retrieval():
    skills = [
        Skill(name="files", path=Path("f.md"), content="# Files\nTools for NAS search and PDF"),
        Skill(name="editing", path=Path("e.md"), content="# Editing\nExcel and Word modifications"),
    ]
    top = retrieve_skills("search NAS pdf files", skills, top_k=1)
    assert top[0].name == "files"
