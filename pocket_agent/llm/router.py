from pathlib import Path
from typing import Any

from pocket_agent.config.models import AppSettings, LlmConfig
from pocket_agent.llm.base import LlmProvider
from pocket_agent.llm.gemini import GeminiProvider
from pocket_agent.llm.ollama import OllamaProvider, RECOMMENDED_OLLAMA_MODELS
from pocket_agent.llm.user_settings import load_llm_user_settings, save_llm_user_settings


class LlmRouter:
    def __init__(
        self,
        llm_config: LlmConfig,
        env: AppSettings,
        cache_dir: Path | None = None,
    ) -> None:
        self._config = llm_config
        self._env = env
        self._cache_dir = cache_dir
        self._providers: dict[str, LlmProvider] = {}
        self._register_available(env)
        self._apply_user_settings()

    def _register_available(self, env: AppSettings) -> None:
        if env.gemini_api_key and "gemini" in self._config.providers:
            cfg = self._config.providers["gemini"]
            self._providers["gemini"] = GeminiProvider(env.gemini_api_key, cfg.model)

        if "ollama" in self._config.providers:
            cfg = self._config.providers["ollama"]
            self._providers["ollama"] = OllamaProvider(cfg.base_url, cfg.model)

    def _apply_user_settings(self) -> None:
        if not self._cache_dir:
            return
        data = load_llm_user_settings(self._cache_dir)
        ollama_model = data.get("ollama_model")
        if ollama_model and "ollama" in self._providers:
            provider = self._providers["ollama"]
            if isinstance(provider, OllamaProvider):
                provider.set_model(str(ollama_model))

    def _user_settings(self) -> dict[str, Any]:
        if not self._cache_dir:
            return {}
        return load_llm_user_settings(self._cache_dir)

    def _save_user_settings(self, patch: dict[str, Any]) -> dict[str, Any]:
        if not self._cache_dir:
            raise RuntimeError("LLM user settings path not configured")
        data = self._user_settings()
        data.update(patch)
        save_llm_user_settings(self._cache_dir, data)
        return data

    def active_reasoning_provider(self) -> str:
        override = self._user_settings().get("reasoning_provider")
        if override and override in self._providers:
            return str(override)
        return self._config.provider_for_task("reasoning")

    def get(self, task_type: str = "default") -> LlmProvider:
        if task_type == "reasoning":
            provider_name = self.active_reasoning_provider()
        else:
            provider_name = self._config.provider_for_task(task_type)

        provider = self._providers.get(provider_name)
        if provider is None:
            if self._providers:
                return next(iter(self._providers.values()))
            raise RuntimeError(
                "No LLM providers configured. Install Ollama and pull a small model "
                "(e.g. gemma3:4b), or set GEMINI_API_KEY."
            )
        return provider

    @property
    def available_providers(self) -> list[str]:
        return list(self._providers.keys())

    def reasoning_model(self) -> str:
        provider = self.get("reasoning")
        if isinstance(provider, OllamaProvider):
            return provider.model
        name = self.active_reasoning_provider()
        cfg = self._config.providers.get(name)
        return cfg.model if cfg else name

    async def describe_providers(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        active = self.active_reasoning_provider()

        for name, provider in self._providers.items():
            cfg = self._config.providers.get(name)
            if isinstance(provider, OllamaProvider):
                model = provider.model
            else:
                model = cfg.model if cfg else ""
            connected = False
            error: str | None = None
            if isinstance(provider, OllamaProvider):
                try:
                    connected = await provider.ping()
                    if not connected:
                        error = "Ollama not reachable at " + provider.base_url
                except Exception as exc:
                    error = str(exc)
            elif name == "gemini":
                connected = bool(self._env.gemini_api_key)
                if not connected:
                    error = "GEMINI_API_KEY not set"

            items.append(
                {
                    "id": name,
                    "label": name.capitalize(),
                    "connected": connected,
                    "model": model,
                    "active": name == active,
                    "error": error,
                }
            )

        return items

    async def list_ollama_models(self) -> list[str]:
        provider = self._providers.get("ollama")
        if not isinstance(provider, OllamaProvider):
            return []
        return await provider.list_models()

    async def pull_ollama_model(self, model: str) -> None:
        provider = self._providers.get("ollama")
        if not isinstance(provider, OllamaProvider):
            raise RuntimeError("Ollama provider is not configured")
        await provider.pull_model(model)
        provider.set_model(model)
        self._save_user_settings({"ollama_model": model, "reasoning_provider": "ollama"})

    def set_reasoning_provider(self, provider_id: str) -> None:
        if provider_id not in self._providers:
            raise ValueError(f"Unknown provider: {provider_id}")
        self._save_user_settings({"reasoning_provider": provider_id})

    def set_ollama_model(self, model: str) -> None:
        provider = self._providers.get("ollama")
        if not isinstance(provider, OllamaProvider):
            raise RuntimeError("Ollama provider is not configured")
        provider.set_model(model)
        self._save_user_settings({"ollama_model": model})

    def recommended_ollama_models(self) -> list[str]:
        return list(RECOMMENDED_OLLAMA_MODELS)
