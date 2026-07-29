"""Write workspace env files and verify local dev prerequisites."""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

from pocket_agent.workspace.paths import find_agent_root, find_workspace_root
from pocket_agent.workspace.user_setup import workspace_auth_mode

logger = logging.getLogger(__name__)


def _upsert_env_line(path: Path, key: str, value: str) -> bool:
    if not value:
        return False
    lines: list[str] = []
    found = False
    if path.is_file():
        lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for line in lines:
        if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
            out.append(f"{key}={value}")
            found = True
        else:
            out.append(line)
    if not found:
        if out and out[-1].strip():
            out.append("")
        out.append(f"{key}={value}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return True


def _copy_example_if_missing(target: Path, example: Path) -> bool:
    if target.exists():
        return False
    if not example.is_file():
        return False
    target.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def write_local_env(
    workspace_root: Path | None = None,
    google_client_id: str | None = None,
    gemini_api_key: str | None = None,
    auth_mode: str | None = None,
) -> list[str]:
    """Sync auth mode, OAuth, and LLM keys across agent, web, and API env files."""
    workspace = workspace_root or find_workspace_root()
    agent = find_agent_root()
    actions: list[str] = []

    mode = auth_mode or workspace_auth_mode(workspace)

    agent_env = agent / ".env"
    agent_example = agent / ".env.example"
    if _copy_example_if_missing(agent_env, agent_example):
        actions.append(f"created:{agent_env.relative_to(workspace)}")

    web_env = workspace / "pocket-agent-web-app" / ".env.local"
    web_example = workspace / "pocket-agent-web-app" / ".env.example"
    if _copy_example_if_missing(web_env, web_example):
        actions.append(f"created:{web_env.relative_to(workspace)}")

    api_env = workspace / "pocket-agent-api-app" / ".dev.vars"
    api_example = workspace / "pocket-agent-api-app" / ".env.example"
    if _copy_example_if_missing(api_env, api_example):
        actions.append(f"created:{api_env.relative_to(workspace)}")

    if _upsert_env_line(agent_env, "AUTH_MODE", mode):
        actions.append(f"updated:pocket-agent/.env AUTH_MODE={mode}")
    if _upsert_env_line(web_env, "VITE_AUTH_MODE", mode):
        actions.append(f"updated:pocket-agent-web-app/.env.local VITE_AUTH_MODE={mode}")
    if _upsert_env_line(api_env, "AUTH_MODE", mode):
        actions.append(f"updated:pocket-agent-api-app/.dev.vars AUTH_MODE={mode}")

    if mode == "google" and google_client_id:
        if _upsert_env_line(agent_env, "GOOGLE_CLIENT_ID", google_client_id):
            actions.append("updated:pocket-agent/.env GOOGLE_CLIENT_ID")
        if _upsert_env_line(web_env, "VITE_GOOGLE_CLIENT_ID", google_client_id):
            actions.append("updated:pocket-agent-web-app/.env.local VITE_GOOGLE_CLIENT_ID")
        if _upsert_env_line(api_env, "GOOGLE_CLIENT_ID", google_client_id):
            actions.append("updated:pocket-agent-api-app/.dev.vars GOOGLE_CLIENT_ID")

    if gemini_api_key:
        if _upsert_env_line(agent_env, "GEMINI_API_KEY", gemini_api_key):
            actions.append("updated:pocket-agent/.env GEMINI_API_KEY")

    return actions


def ensure_desktop_icons(workspace_root: Path | None = None) -> list[str]:
    workspace = workspace_root or find_workspace_root()
    icon_dir = workspace / "pocket-agent-desktop-app" / "src-tauri" / "icons"
    if icon_dir.is_dir() and any(icon_dir.iterdir()):
        return ["skip:desktop-icons:exists"]
    script = workspace / "scripts" / "generate-desktop-icons.sh"
    if not script.is_file():
        return ["error:desktop-icons:no-script"]
    try:
        subprocess.run([str(script)], check=True, cwd=str(workspace))
        return ["ok:desktop-icons"]
    except subprocess.CalledProcessError as exc:
        return [f"error:desktop-icons:{exc}"]


def check_prerequisites(workspace_root: Path | None = None) -> dict:
    workspace = workspace_root or find_workspace_root()
    agent = find_agent_root()

    def has_cmd(name: str) -> bool:
        return shutil.which(name) is not None

    def has_path(rel: str) -> bool:
        return (workspace / rel).exists()

    return {
        "python3": has_cmd("python3"),
        "bun": has_cmd("bun"),
        "npm": has_cmd("npm"),
        "cargo": has_cmd("cargo"),
        "rustc": has_cmd("rustc"),
        "agent_venv": (agent / ".venv").is_dir(),
        "web_node_modules": has_path("pocket-agent-web-app/node_modules"),
        "api_node_modules": has_path("pocket-agent-api-app/node_modules"),
        "desktop_node_modules": has_path("pocket-agent-desktop-app/node_modules"),
        "wizard_built": has_path("pocket-agent-wizard/dist/index.html")
        or has_path("wizard/dist/index.html"),
        "desktop_icons": has_path("pocket-agent-desktop-app/src-tauri/icons/32x32.png"),
        "auth_mode": workspace_auth_mode(workspace),
        "modules": {
            "web": has_path("pocket-agent-web-app/package.json"),
            "api": has_path("pocket-agent-api-app/package.json"),
            "desktop": has_path("pocket-agent-desktop-app/package.json"),
            "agent": has_path("pocket-agent/pyproject.toml"),
        },
    }


def run_bootstrap(
    workspace_root: Path | None = None,
    google_client_id: str | None = None,
    gemini_api_key: str | None = None,
    use_desktop: bool = False,
    generate_icons: bool = True,
    auth_mode: str | None = None,
) -> dict:
    workspace = workspace_root or find_workspace_root()
    result: dict = {"actions": [], "prereqs": check_prerequisites(workspace)}

    result["actions"].extend(
        write_local_env(
            workspace,
            google_client_id=google_client_id,
            gemini_api_key=gemini_api_key,
            auth_mode=auth_mode,
        )
    )

    if use_desktop and generate_icons:
        result["actions"].extend(ensure_desktop_icons(workspace))

    result["use_desktop"] = use_desktop
    result["auth_mode"] = auth_mode or workspace_auth_mode(workspace)
    return result
