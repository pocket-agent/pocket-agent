"""Resolve workspace (org folder) vs agent repo roots."""

from __future__ import annotations

from pathlib import Path

MODULES_FILE = Path("config/modules.yaml")
SETUP_DEFAULTS = Path("config/setup.defaults.yaml")
AGENT_NESTED = Path("pocket-agent")


def find_agent_root(start: Path | None = None) -> Path:
    """Directory containing pyproject.toml and pocket_agent package."""
    start = start or Path.cwd()
    for path in [start, *start.parents]:
        if _is_agent_root(path):
            return path
        nested = path / AGENT_NESTED
        if _is_agent_root(nested):
            return nested
    return start


def find_workspace_root(start: Path | None = None) -> Path:
    """Org folder: config/modules.yaml or setup.defaults + nested agent."""
    start = start or Path.cwd()
    agent = find_agent_root(start)
    if _is_agent_root(agent) and (agent.parent / MODULES_FILE).is_file():
        return agent.parent
    for path in [start, *start.parents]:
        if (path / MODULES_FILE).is_file():
            return path
        if (path / SETUP_DEFAULTS).is_file() and (path / AGENT_NESTED / "pyproject.toml").is_file():
            return path
    return agent.parent if _is_agent_root(agent) else start


def _is_agent_root(path: Path) -> bool:
    return (path / "pyproject.toml").is_file() and (path / "pocket_agent").is_dir()
