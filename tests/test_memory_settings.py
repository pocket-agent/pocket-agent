from pathlib import Path

from pocket_agent.config.models import AppSettings, PathsConfig
from pocket_agent.memory.service import MemoryService


def test_personal_memory_toggle_and_clear(tmp_path: Path):
    paths = PathsConfig(
        {
            "data": {"cache": "data/cache", "logs": "data/logs"},
            "memory": {"db_path": "data/cache/memory.db"},
        },
        tmp_path,
    )
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    env = AppSettings()
    memory = MemoryService(paths, env)

    memory.set_personal_memory_enabled(True)
    assert memory.is_personal_memory_enabled()

    import asyncio

    async def _remember():
        return await memory.remember(1, "likes tea", category="preference")

    result = asyncio.run(_remember())
    assert not isinstance(result, str)
    assert memory.personal.count() == 1

    memory.set_personal_memory_enabled(False)
    assert not memory.is_personal_memory_enabled()

    async def _remember_disabled():
        return await memory.remember(1, "should fail")

    err = asyncio.run(_remember_disabled())
    assert err == "Personal memory is disabled in settings"

    deleted = memory.clear_personal_memories()
    assert deleted == 1
    assert memory.personal.count() == 0
