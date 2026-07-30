"""Persist user preferences for personal memory (not knowledge base)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_FILENAME = "memory-user-settings.json"


def _settings_path(cache_dir: Path) -> Path:
    return cache_dir / DEFAULT_FILENAME


def load_memory_user_settings(cache_dir: Path) -> dict[str, Any]:
    path = _settings_path(cache_dir)
    if not path.is_file():
        return {"enabled": True}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"enabled": True}
        if "enabled" not in data:
            data["enabled"] = True
        return data
    except (json.JSONDecodeError, OSError):
        return {"enabled": True}


def save_memory_user_settings(cache_dir: Path, data: dict[str, Any]) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = _settings_path(cache_dir)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def personal_memory_enabled(cache_dir: Path) -> bool:
    return bool(load_memory_user_settings(cache_dir).get("enabled", True))


def set_personal_memory_enabled(cache_dir: Path, enabled: bool) -> None:
    data = load_memory_user_settings(cache_dir)
    data["enabled"] = enabled
    save_memory_user_settings(cache_dir, data)
