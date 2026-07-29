import httpx

from pocket_agent.llm.base import LlmProvider, LlmResponse


class OllamaProvider(LlmProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def complete(self, prompt: str, system: str | None = None) -> LlmResponse:
        payload: dict = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{self._base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()

        text = data.get("response", "")
        return LlmResponse(text=text, provider=self.name, model=self._model, raw=data)
