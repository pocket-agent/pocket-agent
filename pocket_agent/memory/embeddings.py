from google import genai

from pocket_agent.config.models import AppSettings, PathsConfig


class EmbeddingService:
    def __init__(self, paths: PathsConfig, env: AppSettings) -> None:
        self._model = paths.embedding_model
        self._client: genai.Client | None = None
        if env.gemini_api_key:
            self._client = genai.Client(api_key=env.gemini_api_key)

    @property
    def available(self) -> bool:
        return self._client is not None

    async def embed(self, text: str) -> list[float] | None:
        if not self._client or not text.strip():
            return None
        try:
            response = await self._client.aio.models.embed_content(
                model=self._model,
                contents=text[:8000],
            )
            if response.embeddings:
                return list(response.embeddings[0].values)
        except Exception:
            return None
        return None
