"""Clone pocket-agent app repos into apps/ (nested git projects)."""

from __future__ import annotations

import logging
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

SCaffold_FILES = frozenset({"README.md", ".gitkeep"})


def find_project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "config").is_dir():
        return cwd
    candidate = Path(__file__).resolve().parents[3]
    if (candidate / "config").is_dir():
        return candidate
    return cwd


def load_apps_config(project_root: Path) -> dict:
    config_path = project_root / "config" / "apps.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing {config_path}")
    with config_path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def is_scaffold_only(path: Path) -> bool:
    if not path.exists():
        return True
    if not path.is_dir():
        return False
    for child in path.iterdir():
        if child.name in Scaffold_FILES:
            continue
        if child.name == ".git":
            continue
        return False
    return True


def clear_scaffold(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return
    for child in path.iterdir():
        if child.name in Scaffold_FILES:
            child.unlink()
        elif child.name == ".git" and child.is_dir():
            shutil.rmtree(child)


def clone_repo(repo_url: str, target: Path, branch: str | None = None) -> None:
    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo_url, str(target)])
    subprocess.run(cmd, check=True)


def init_app(
    name: str,
    spec: dict,
    project_root: Path,
    force: bool = False,
) -> str:
    rel_path = spec.get("path", f"apps/{name}")
    target = project_root / rel_path
    repo = spec.get("repo", "")
    enabled = spec.get("enabled", True)

    if not enabled:
        return f"skip:{name}:disabled"

    if not repo:
        return f"skip:{name}:no-repo"

    if target.exists() and not is_scaffold_only(target):
        if not force:
            logger.info("Skipping %s — %s already exists and is not empty", name, rel_path)
            return f"skip:{name}:exists"
        logger.warning("Removing existing %s (--force)", rel_path)
        shutil.rmtree(target)

    if target.exists():
        clear_scaffold(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Cloning %s into %s", repo, rel_path)
    clone_repo(repo, target)
    return f"ok:{name}"


def run_init(
    project_root: Path | None = None,
    only: str = "all",
    force: bool = False,
    skip_setup: bool = False,
) -> int:
    root = project_root or find_project_root()

    if not skip_setup:
        from pocket_agent.cli.setup_wizard import run_setup

        setup_code = run_setup(project_root=root, force=False)
        if setup_code != 0:
            return setup_code

    config = load_apps_config(root)
    apps = config.get("apps", {})

    names = list(apps.keys())
    if only != "all":
        if only not in apps:
            logger.error("Unknown app %r. Choices: %s", only, ", ".join(names))
            return 1
        names = [only]

    results: list[str] = []
    for name in names:
        spec = apps[name]
        try:
            results.append(init_app(name, spec, root, force=force))
        except subprocess.CalledProcessError as exc:
            logger.error("Failed to clone %s: %s", name, exc)
            return 1
        except Exception as exc:
            logger.error("Failed to init %s: %s", name, exc)
            return 1

    for result in results:
        logger.info(result)

    logger.info(
        "Done. Each app is a nested git repo — commit inside apps/web or apps/api separately."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="pocket-agent init",
        description="Clone pocket-agent app repositories into apps/",
    )
    parser.add_argument(
        "--only",
        choices=["web", "api", "cli", "all"],
        default="all",
        help="Clone only one app (default: all enabled apps)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace scaffold or existing directory (destructive)",
    )
    parser.add_argument(
        "--skip-setup",
        action="store_true",
        help="Skip writing config/user-setup.yaml (all-local defaults)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return run_init(only=args.only, force=args.force, skip_setup=args.skip_setup)


if __name__ == "__main__":
    sys.exit(main())
