"""First-time setup wizard — writes workspace config/user-setup.yaml."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from pocket_agent_sdk import CONNECTION_PROFILES
from pocket_agent.workspace.paths import find_workspace_root

logger = logging.getLogger(__name__)

SETUP_REL = Path("config/user-setup.yaml")
DEFAULTS_REL = Path("config/setup.defaults.yaml")


def run_setup(
    workspace_root: Path | None = None,
    force: bool = False,
    profile: str | None = None,
    overrides: dict | None = None,
) -> int:
    root = workspace_root or find_workspace_root()
    target = root / SETUP_REL
    defaults = root / DEFAULTS_REL

    if not defaults.is_file():
        logger.error("Missing %s", defaults)
        return 1

    if target.exists() and not force and not overrides:
        logger.info("Setup already exists at %s (use --force to overwrite)", SETUP_REL)
        return 0

    with defaults.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    if profile:
        data["profile"] = profile

    if overrides:
        data = _deep_merge(data, overrides)

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, default_flow_style=False, sort_keys=False)

    logger.info("Created %s (profile: %s)", SETUP_REL, data.get("profile", "all-local"))
    logger.info(
        "Stack: web %s → api %s → agent %s",
        data.get("web", {}).get("url"),
        data.get("api", {}).get("url"),
        data.get("agent", {}).get("url"),
    )
    logger.info("Next: pocket-agent init  # install modules from latest releases")
    return 0


def _deep_merge(base: dict, patch: dict) -> dict:
    out = dict(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="pocket-agent setup",
        description="Write config/user-setup.yaml (all-local by default)",
    )
    parser.add_argument(
        "--profile",
        choices=list(CONNECTION_PROFILES),
        default=None,
        help="Override profile",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing user-setup.yaml",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return run_setup(force=args.force, profile=args.profile)


if __name__ == "__main__":
    import sys

    sys.exit(main())
