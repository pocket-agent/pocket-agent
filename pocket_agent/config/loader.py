import yaml
from pathlib import Path

from pocket_agent.config.models import (
    AppSettings,
    LlmConfig,
    PathsConfig,
    SettingsBundle,
)


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_settings(project_root: Path | None = None) -> SettingsBundle:
    root = project_root or Path.cwd()
    config_dir = root / "config"

    paths_data = _load_yaml(config_dir / "paths.yaml")
    llm_data = _load_yaml(config_dir / "llm.yaml")
    settings_data = _load_yaml(config_dir / "settings.yaml")

    env = AppSettings()
    paths = PathsConfig(paths_data, root)

    if env.nas_root:
        paths.nas_root = Path(env.nas_root).expanduser()
        if paths.nas_root not in paths.allowed_read_roots:
            paths.allowed_read_roots.insert(0, paths.nas_root)

    return SettingsBundle(
        env=env,
        paths=paths,
        llm=LlmConfig(llm_data),
        raw_settings=settings_data,
    )


def ensure_data_dirs(paths: PathsConfig) -> None:
    for directory in (
        paths.data_root,
        paths.logs_dir,
        paths.working_dir,
        paths.backup_dir,
        paths.cache_dir,
        paths.queue_dir,
        paths.memory_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)
