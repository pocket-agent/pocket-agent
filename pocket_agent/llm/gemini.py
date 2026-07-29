from google import genai
from google.genai import types

from pocket_agent.llm.base import LlmProvider, LlmResponse


class GeminiProvider(LlmProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def complete(self, prompt: str, system: str | None = None) -> LlmResponse:
        config = types.GenerateContentConfig(system_instruction=system) if system else None

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )
        text = response.text or ""
        return LlmResponse(text=text, provider=self.name, model=self._model, raw=response)
