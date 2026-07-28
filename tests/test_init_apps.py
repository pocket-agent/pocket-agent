"""Tests for monorepo app init (scaffold detection)."""

from pathlib import Path

from pocket_agent.cli.init_apps import is_scaffold_only


def test_is_scaffold_only_empty_dir(tmp_path: Path):
    assert is_scaffold_only(tmp_path) is True


def test_is_scaffold_only_readme_and_gitkeep(tmp_path: Path):
    (tmp_path / "README.md").write_text("hi")
    (tmp_path / ".gitkeep").write_text("")
    assert is_scaffold_only(tmp_path) is True


def test_is_scaffold_only_with_package_json(tmp_path: Path):
    (tmp_path / "README.md").write_text("hi")
    (tmp_path / "package.json").write_text("{}")
    assert is_scaffold_only(tmp_path) is False
