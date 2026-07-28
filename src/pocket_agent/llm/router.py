from pocket_agent.config.models import AppSettings, LlmConfig
from pocket_agent.llm.base import LlmProvider
from pocket_agent.llm.gemini import GeminiProvider
from pocket_agent.llm.ollama import OllamaProvider


class LlmRouter:
    def __init__(self, llm_config: LlmConfig, env: AppSettings) -> None:
        self._config = llm_config
        self._providers: dict[str, LlmProvider] = {}
        self._register_available(env)

    def _register_available(self, env: AppSettings) -> None:
        if env.gemini_api_key and "gemini" in self._config.providers:
            cfg = self._config.providers["gemini"]
            self._providers["gemini"] = GeminiProvider(env.gemini_api_key, cfg.model)

        if "ollama" in self._config.providers:
            cfg = self._config.providers["ollama"]
            self._providers["ollama"] = OllamaProvider(cfg.base_url, cfg.model)

    def get(self, task_type: str = "default") -> LlmProvider:
        provider_name = self._config.provider_for_task(task_type)
        provider = self._providers.get(provider_name)
        if provider is None:
            if self._providers:
                return next(iter(self._providers.values()))
            raise RuntimeError(
                "No LLM providers configured. Set GEMINI_API_KEY or ensure Ollama is reachable."
            )
        return provider

    @property
    def available_providers(self) -> list[str]:
        return list(self._providers.keys())
