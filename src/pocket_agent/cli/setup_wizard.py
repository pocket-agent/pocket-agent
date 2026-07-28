"""First-time setup wizard — defaults to all-local profile."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from pocket_agent.cli.init_apps import find_project_root

logger = logging.getLogger(__name__)

SETUP_REL = Path("config/user-setup.yaml")
DEFAULTS_REL = Path("config/setup.defaults.yaml")


def run_setup(
    project_root: Path | None = None,
    force: bool = False,
    profile: str | None = None,
) -> int:
    root = project_root or find_project_root()
    target = root / SETUP_REL
    defaults = root / DEFAULTS_REL

    if not defaults.is_file():
        logger.error("Missing %s", defaults)
        return 1

    if target.exists() and not force:
        logger.info("Setup already exists at %s (use --force to overwrite)", SETUP_REL)
        return 0

    with defaults.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    if profile:
        data["profile"] = profile

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, default_flow_style=False, sort_keys=False)

    logger.info("Created %s (profile: %s)", SETUP_REL, data.get("profile", "all-local"))
    logger.info(
        "Local stack: web %s → api %s → agent %s",
        data.get("web", {}).get("url"),
        data.get("api", {}).get("url"),
        data.get("agent", {}).get("url"),
    )
    logger.info("Next: pocket-agent init  # clone apps/web + apps/api (Hono template)")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="pocket-agent setup",
        description="Write config/user-setup.yaml (all-local by default)",
    )
    parser.add_argument(
        "--profile",
        choices=["all-local", "hosted-ui-home-agent", "cloud-only"],
        default=None,
        help="Override profile (default: all-local from setup.defaults.yaml)",
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
