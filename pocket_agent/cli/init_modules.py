"""Install pocket-agent module repos as sibling projects (release tarball or git)."""

from __future__ import annotations

import logging
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Literal

import httpx
import yaml

from pocket_agent.workspace.paths import find_workspace_root

logger = logging.getLogger(__name__)

SCaffold_FILES = frozenset({"README.md", ".gitkeep"})
SourceMode = Literal["release", "git"]


def load_modules_config(workspace_root: Path) -> dict:
    config_path = workspace_root / "config" / "modules.yaml"
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


def parse_github_slug(slug: str) -> tuple[str, str]:
    owner, repo = slug.split("/", 1)
    return owner, repo


def fetch_latest_release_tag(owner: str, repo: str) -> str | None:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = httpx.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=30.0,
            follow_redirects=True,
        )
    except httpx.HTTPError as exc:
        logger.warning("Release lookup failed for %s/%s: %s", owner, repo, exc)
        return None
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        logger.warning(
            "Release lookup %s/%s returned %s",
            owner,
            repo,
            response.status_code,
        )
        return None
    data = response.json()
    tag = data.get("tag_name")
    return str(tag) if tag else None


def download_release_tarball(owner: str, repo: str, tag: str, dest_dir: Path) -> Path:
    """Download and extract github.com/{owner}/{repo} release archive into dest_dir."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{owner}/{repo}/archive/refs/tags/{tag}.tar.gz"
    logger.info("Fetching release %s from %s", tag, url)
    with httpx.stream("GET", url, timeout=120.0, follow_redirects=True) as response:
        if response.status_code != 200:
            raise RuntimeError(f"Download failed ({response.status_code}): {url}")
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            for chunk in response.iter_bytes():
                tmp.write(chunk)
    try:
        with tarfile.open(tmp_path, "r:gz") as archive:
            members = archive.getmembers()
            if not members:
                raise RuntimeError(f"Empty archive for {owner}/{repo}@{tag}")
            top = members[0].name.split("/", 1)[0]
            extract_parent = dest_dir.parent
            archive.extractall(extract_parent)
            extracted = extract_parent / top
            target = dest_dir
            if target.exists():
                shutil.rmtree(target)
            extracted.rename(target)
            return target
    finally:
        tmp_path.unlink(missing_ok=True)


def clone_repo(repo_url: str, target: Path, branch: str | None = None) -> None:
    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo_url, str(target)])
    subprocess.run(cmd, check=True)


def install_module(
    name: str,
    spec: dict,
    workspace_root: Path,
    force: bool = False,
    source: SourceMode = "release",
) -> str:
    rel_path = spec.get("path", f"pocket-agent-{name}")
    target = workspace_root / rel_path
    github = spec.get("github", "")
    enabled = spec.get("enabled", True)

    if not enabled:
        return f"skip:{name}:disabled"

    if not github:
        return f"skip:{name}:no-github"

    if target.exists() and not is_scaffold_only(target):
        if not force:
            logger.info("Skipping %s — %s already exists", name, rel_path)
            return f"skip:{name}:exists"
        logger.warning("Removing existing %s (--force)", rel_path)
        shutil.rmtree(target)

    if target.exists():
        clear_scaffold(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    owner, repo = parse_github_slug(github)
    repo_url = f"https://github.com/{owner}/{repo}.git"

    if source == "release":
        tag = fetch_latest_release_tag(owner, repo)
        if tag:
            download_release_tarball(owner, repo, tag, target)
            logger.info("Installed %s@%s into %s", name, tag, rel_path)
            return f"ok:{name}:release:{tag}"
        logger.info("No release for %s/%s — falling back to git clone", owner, repo)
        source = "git"

    if target.exists():
        shutil.rmtree(target)
    clone_repo(repo_url, target)
    logger.info("Cloned %s into %s", repo_url, rel_path)
    return f"ok:{name}:git"


def run_init(
    workspace_root: Path | None = None,
    only: str = "all",
    force: bool = False,
    skip_setup: bool = False,
    source: SourceMode = "release",
    modules: list[str] | None = None,
) -> int:
    root = workspace_root or find_workspace_root()

    if not skip_setup:
        from pocket_agent.cli.setup_wizard import run_setup

        setup_code = run_setup(workspace_root=root, force=False)
        if setup_code != 0:
            return setup_code

    config = load_modules_config(root)
    module_specs = config.get("modules", {})

    names = list(module_specs.keys())
    if only != "all":
        if only not in module_specs:
            logger.error("Unknown module %r. Choices: %s", only, ", ".join(names))
            return 1
        names = [only]

    if modules:
        unknown = [m for m in modules if m not in module_specs]
        if unknown:
            logger.error("Unknown modules: %s", ", ".join(unknown))
            return 1
        names = modules

    results: list[str] = []
    for name in names:
        spec = module_specs[name]
        try:
            results.append(
                install_module(name, spec, root, force=force, source=source)
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Failed to install %s: %s", name, exc)
            return 1
        except Exception as exc:
            logger.error("Failed to install %s: %s", name, exc)
            return 1

    for result in results:
        logger.info(result)

    logger.info(
        "Done. Each module is a separate project — commit inside pocket-agent-app, "
        "pocket-agent-cli, etc."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="pocket-agent init",
        description="Install pocket-agent modules as sibling repos (latest release or git)",
    )
    parser.add_argument(
        "--only",
        default="all",
        help="Install one module by name, or 'all' (default)",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        metavar="NAME",
        help="Install specific modules (overrides --only)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace scaffold or existing directory (destructive)",
    )
    parser.add_argument(
        "--skip-setup",
        action="store_true",
        help="Skip writing config/user-setup.yaml",
    )
    parser.add_argument(
        "--source",
        choices=["release", "git"],
        default="release",
        help="Install from latest GitHub release tarball (default) or shallow git clone",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return run_init(
        only=args.only,
        force=args.force,
        skip_setup=args.skip_setup,
        source=args.source,
        modules=args.modules,
    )


if __name__ == "__main__":
    sys.exit(main())
