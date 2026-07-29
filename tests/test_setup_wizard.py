"""Tests for setup wizard."""

from pathlib import Path

from pocket_agent.cli.setup_wizard import run_setup


def test_run_setup_creates_user_config(tmp_path: Path):
    # Minimal project root
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "setup.defaults.yaml").write_text(
        "profile: all-local\nweb:\n  mode: local\n  url: http://localhost:5173\n"
    )

    code = run_setup(workspace_root=tmp_path, force=True)
    assert code == 0

    user_setup = (tmp_path / "config" / "user-setup.yaml").read_text()
    assert "all-local" in user_setup


def test_run_setup_skips_if_exists(tmp_path: Path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "setup.defaults.yaml").write_text("profile: all-local\n")
    (config_dir / "user-setup.yaml").write_text("profile: custom\n")

    code = run_setup(workspace_root=tmp_path, force=False)
    assert code == 0
    assert "custom" in (config_dir / "user-setup.yaml").read_text()
