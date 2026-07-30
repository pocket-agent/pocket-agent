import httpx

from pocket_agent.llm.base import LlmProvider, LlmResponse

DEFAULT_OLLAMA_URL = "http://localhost:11434"

# Small models suited to ~8GB RAM (Apple Silicon).
RECOMMENDED_OLLAMA_MODELS = [
    "gemma3:4b",
    "qwen3:4b",
    "qwen2.5:3b",
    "qwen2.5:1.5b",
    "llama3.2:3b",
]


class OllamaProvider(LlmProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = (base_url or DEFAULT_OLLAMA_URL).rstrip("/")
        self._model = model

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def model(self) -> str:
        return self._model

    def set_model(self, model: str) -> None:
        self._model = model.strip()

    async def ping(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"{self._base_url}/api/tags")
                return res.status_code == 200
        except httpx.HTTPError:
            return False

    async def list_models(self) -> list[str]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f"{self._base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
        models = data.get("models") or []
        names: list[str] = []
        for item in models:
            name = item.get("name")
            if name:
                names.append(str(name))
        return sorted(names)

    async def pull_model(self, model: str) -> None:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{self._base_url}/api/pull",
                json={"name": model, "stream": False},
            )
            response.raise_for_status()

    async def complete(self, prompt: str, system: str | None = None) -> LlmResponse:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={"model": self._model, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            data = response.json()

        message = data.get("message") or {}
        text = message.get("content", "") or data.get("response", "")
        return LlmResponse(text=text, provider=self.name, model=self._model, raw=data)
