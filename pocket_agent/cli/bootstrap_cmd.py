"""CLI: pocket-agent bootstrap — env files and desktop prep."""

from __future__ import annotations

import argparse
import json
import logging
import sys

from pocket_agent.cli.workspace_bootstrap import run_bootstrap
from pocket_agent.workspace.paths import find_workspace_root

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pocket-agent bootstrap",
        description="Create env files from examples and prepare desktop icons",
    )
    parser.add_argument("--client-id", help="Google OAuth client ID (all env files)")
    parser.add_argument("--gemini-key", help="GEMINI_API_KEY for agent .env")
    parser.add_argument("--desktop", action="store_true", help="Generate Tauri icons")
    parser.add_argument("--icons", action="store_true", help="Generate Tauri icons (alias)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    workspace = find_workspace_root()
    result = run_bootstrap(
        workspace_root=workspace,
        google_client_id=args.client_id,
        gemini_api_key=args.gemini_key,
        use_desktop=args.desktop or args.icons,
        generate_icons=args.desktop or args.icons,
    )
    for action in result.get("actions", []):
        logger.info("%s", action)
    if args.client_id is None and args.gemini_key is None and not (args.desktop or args.icons):
        logger.info("Created missing env templates (no keys provided)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
