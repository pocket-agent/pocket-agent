from google import genai
import httpx
import logging

from pocket_agent.config.models import AppSettings, LlmConfig, PathsConfig

logger = logging.getLogger(__name__)

_GEMINI_EMBED_MODELS = ("gemini-embedding-001", "text-embedding-004")


class EmbeddingService:
    def __init__(
        self,
        paths: PathsConfig,
        env: AppSettings,
        llm: LlmConfig | None = None,
    ) -> None:
        self._configured = paths.embedding_model
        self._client: genai.Client | None = None
        if env.gemini_api_key:
            self._client = genai.Client(api_key=env.gemini_api_key)

        ollama = (llm.providers.get("ollama") if llm else None)
        self._ollama_base = (
            env.ollama_base_url
            or (ollama.base_url if ollama else "")
            or "http://localhost:11434"
        ).rstrip("/")
        self._ollama_embed_model = env.ollama_embed_model

    @property
    def available(self) -> bool:
        return self._client is not None or bool(self._ollama_base)

    async def _embed_gemini(self, text: str) -> list[float] | None:
        if not self._client:
            return None
        models = [self._configured]
        for name in _GEMINI_EMBED_MODELS:
            if name not in models:
                models.append(name)

        for model in models:
            try:
                response = await self._client.aio.models.embed_content(
                    model=model,
                    contents=text[:8000],
                )
                if response.embeddings:
                    return list(response.embeddings[0].values)
            except Exception as exc:
                logger.warning("Gemini embed failed model=%s: %s", model, exc)
        return None

    async def _embed_ollama(self, text: str) -> list[float] | None:
        url = f"{self._ollama_base}/api/embeddings"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url,
                    json={"model": self._ollama_embed_model, "prompt": text[:8000]},
                )
                if response.status_code != 200:
                    logger.warning("Ollama embed HTTP %s", response.status_code)
                    return None
                data = response.json()
                embedding = data.get("embedding")
                if isinstance(embedding, list) and embedding:
                    return [float(x) for x in embedding]
        except Exception as exc:
            logger.warning("Ollama embed failed: %s", exc)
        return None

    async def embed(self, text: str) -> list[float] | None:
        if not text.strip():
            return None

        vector = await self._embed_gemini(text)
        if vector:
            return vector
        return await self._embed_ollama(text)
