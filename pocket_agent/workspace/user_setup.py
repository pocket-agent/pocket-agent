"""Read workspace config/user-setup.yaml merged with defaults."""

from __future__ import annotations

from pathlib import Path

import yaml

try:
    from pocket_agent_sdk.auth import resolve_auth_mode
except ImportError:
    resolve_auth_mode = None  # type: ignore[assignment,misc]


def load_workspace_setup(workspace: Path) -> dict:
    defaults_path = workspace / "config" / "setup.defaults.yaml"
    setup_path = workspace / "config" / "user-setup.yaml"
    data: dict = {}
    if defaults_path.is_file():
        with defaults_path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    if setup_path.is_file():
        with setup_path.open(encoding="utf-8") as fh:
            user = yaml.safe_load(fh) or {}
            data = {**data, **user}
    return data


def workspace_auth_mode(workspace: Path) -> str:
    data = load_workspace_setup(workspace)
    auth = data.get("auth") or {}
    mode = auth.get("mode")
    if mode in ("none", "google"):
        return str(mode)
    if resolve_auth_mode is not None:
        return resolve_auth_mode(
            data.get("profile"),
            (data.get("web") or {}).get("mode"),
            (data.get("api") or {}).get("mode"),
        )
    profile = data.get("profile", "all-local")
    web_mode = (data.get("web") or {}).get("mode", "local")
    api_mode = (data.get("api") or {}).get("mode", "local")
    if profile == "all-local" and web_mode == "local" and api_mode == "local":
        return "none"
    return "google"
