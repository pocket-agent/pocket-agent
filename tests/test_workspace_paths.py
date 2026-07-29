"""Tests for workspace path resolution."""

from pathlib import Path

from pocket_agent.workspace.paths import find_sdk_root, find_wizard_dist, find_wizard_root


def test_find_wizard_paths_in_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "org"
    wizard = workspace / "pocket-agent-wizard"
    dist = wizard / "dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_text("<html></html>", encoding="utf-8")
    (wizard / "package.json").write_text("{}", encoding="utf-8")

    assert find_wizard_root(workspace) == wizard
    assert find_wizard_dist(workspace) == dist


def test_find_sdk_root(tmp_path: Path) -> None:
    workspace = tmp_path / "org"
    sdk = workspace / "pocket-agent-sdk"
    sdk.mkdir(parents=True)
    (sdk / "package.json").write_text("{}", encoding="utf-8")

    assert find_sdk_root(workspace) == sdk
