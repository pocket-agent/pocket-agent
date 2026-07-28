from pathlib import Path

import pytest

from pocket_agent.config.loader import ensure_data_dirs, load_settings


def test_load_settings_from_repo_root():
    root = Path(__file__).resolve().parents[1]
    settings = load_settings(root)

    assert settings.llm.default_provider == "gemini"
    assert settings.paths.skills_dir == root / "agent" / "skills"
    assert settings.paths.prompts_dir == root / "agent" / "prompts"


def test_ensure_data_dirs(tmp_path: Path):
    from pocket_agent.config.models import PathsConfig

    paths = PathsConfig(
        {
            "data": {
                "root": "data",
                "logs": "data/logs",
                "working": "data/working",
                "backup": "data/backup",
                "cache": "data/cache",
                "queue": "data/queue",
            },
            "agent": {"memory_dir": "agent/memory"},
        },
        tmp_path,
    )
    ensure_data_dirs(paths)
    assert paths.logs_dir.is_dir()
    assert paths.working_dir.is_dir()
