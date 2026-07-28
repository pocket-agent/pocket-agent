from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    telegram_allowed_user_ids: str = Field(default="", alias="TELEGRAM_ALLOWED_USER_IDS")
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    nas_root: str = Field(default="", alias="NAS_ROOT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    def allowed_user_ids(self) -> set[int]:
        if not self.telegram_allowed_user_ids.strip():
            return set()
        return {int(x.strip()) for x in self.telegram_allowed_user_ids.split(",") if x.strip()}


class PathsConfig:
    def __init__(self, data: dict[str, Any], project_root: Path) -> None:
        self.project_root = project_root
        nas = data.get("nas", {})
        data_paths = data.get("data", {})
        agent = data.get("agent", {})
        index = data.get("index", {})

        nas_root = nas.get("root", "")
        self.nas_root = Path(nas_root).expanduser()
        self.allowed_read_roots = [
            Path(p).expanduser() for p in nas.get("allowed_read_roots", [])
        ]

        self.data_root = project_root / data_paths.get("root", "data")
        self.logs_dir = project_root / data_paths.get("logs", "data/logs")
        self.working_dir = project_root / data_paths.get("working", "data/working")
        self.backup_dir = project_root / data_paths.get("backup", "data/backup")
        self.cache_dir = project_root / data_paths.get("cache", "data/cache")
        self.queue_dir = project_root / data_paths.get("queue", "data/queue")
        self.index_db_path = project_root / index.get("db_path", "data/cache/file_index.db")
        self.index_max_depth = int(index.get("max_depth", 12))
        self.index_exclude_dirs = set(index.get("exclude_dir_names", []))

        self.skills_dir = project_root / agent.get("skills_dir", "agent/skills")
        self.prompts_dir = project_root / agent.get("prompts_dir", "agent/prompts")
        self.memory_dir = project_root / agent.get("memory_dir", "agent/memory")


class LlmProviderConfig:
    def __init__(self, name: str, data: dict[str, Any]) -> None:
        self.name = name
        self.model = data.get("model", "")
        self.base_url = data.get("base_url", "")


class LlmConfig:
    def __init__(self, data: dict[str, Any]) -> None:
        self.default_provider = data.get("default_provider", "gemini")
        self.routing = data.get("routing", {})
        self.providers = {
            name: LlmProviderConfig(name, cfg)
            for name, cfg in data.get("providers", {}).items()
        }

    def provider_for_task(self, task_type: str) -> str:
        return self.routing.get(task_type, self.routing.get("default", self.default_provider))


class SettingsBundle:
    def __init__(
        self,
        env: AppSettings,
        paths: PathsConfig,
        llm: LlmConfig,
        raw_settings: dict[str, Any],
    ) -> None:
        self.env = env
        self.paths = paths
        self.llm = llm
        self.raw_settings = raw_settings
