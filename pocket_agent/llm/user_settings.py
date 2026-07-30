"""Persist user-selected LLM provider (runtime override)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_FILENAME = "llm-user-settings.json"


def _settings_path(cache_dir: Path) -> Path:
    return cache_dir / DEFAULT_FILENAME


def load_llm_user_settings(cache_dir: Path) -> dict[str, Any]:
    path = _settings_path(cache_dir)
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_llm_user_settings(cache_dir: Path, data: dict[str, Any]) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = _settings_path(cache_dir)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
