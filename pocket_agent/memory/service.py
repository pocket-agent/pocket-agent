from pocket_agent.config.models import AppSettings, LlmConfig, PathsConfig
from pocket_agent.core.skill_loader import Skill
from pocket_agent.memory.db import MemoryDatabase
from pocket_agent.memory.embeddings import EmbeddingService
from pocket_agent.memory.knowledge import KnowledgeBase
from pocket_agent.memory.personal import PersonalMemory, PersonalMemoryStore
from pocket_agent.memory.skill_retrieval import retrieve_skills
from pocket_agent.memory.user_settings import (
    personal_memory_enabled,
    set_personal_memory_enabled,
)


class MemoryService:
    def __init__(self, paths: PathsConfig, env: AppSettings, llm: LlmConfig | None = None) -> None:
        self._paths = paths
        self._db = MemoryDatabase(paths.memory_db_path)
        self._personal = PersonalMemoryStore(self._db)
        self._knowledge = KnowledgeBase(self._db, chunk_size=paths.memory_chunk_size)
        self._embeddings = EmbeddingService(paths, env, llm=llm)
        self._skill_top_k = paths.skill_top_k
        self._vector_limit = paths.vector_search_limit

    @property
    def knowledge(self) -> KnowledgeBase:
        return self._knowledge

    @property
    def personal(self) -> PersonalMemoryStore:
        return self._personal

    @property
    def embeddings_available(self) -> bool:
        return self._embeddings.available

    def is_personal_memory_enabled(self) -> bool:
        return personal_memory_enabled(self._paths.cache_dir)

    def set_personal_memory_enabled(self, enabled: bool) -> None:
        set_personal_memory_enabled(self._paths.cache_dir, enabled)

    def clear_personal_memories(self) -> int:
        return self._personal.clear_all()

    async def remember(self, user_id: int, content: str, category: str = "preference") -> PersonalMemory | str:
        if not self.is_personal_memory_enabled():
            return "Personal memory is disabled in settings"

        result = self._personal.add(user_id, content, category=category)
        if isinstance(result, str):
            return result

        vector = await self._embeddings.embed(content)
        if vector:
            self._db.store_embedding("memory", result.id, vector)
        return result

    async def recall(self, query: str, user_id: int | None = None, limit: int = 5) -> list[PersonalMemory]:
        if not self.is_personal_memory_enabled():
            return []

        fts_results = self._personal.search_fts(query, user_id=user_id, limit=limit)
        if fts_results:
            return fts_results

        vector = await self._embeddings.embed(query)
        if not vector:
            return []

        hits = self._db.vector_search(vector, "memory", limit=limit)
        ids = [entity_id for entity_id, score in hits if score > 0.1]
        return self._personal.get_by_ids(ids)

    async def search_knowledge(self, query: str, limit: int = 5) -> list:
        fts_results = self._knowledge.search_fts(query, limit=limit)
        if fts_results:
            return fts_results

        vector = await self._embeddings.embed(query)
        if not vector:
            return []

        hits = self._db.vector_search(vector, "knowledge", limit=limit)
        ids = [entity_id for entity_id, score in hits if score > 0.1]
        return self._knowledge.get_by_ids(ids)

    async def index_knowledge_chunk(self, source_path: str, text: str) -> int:
        count = self._knowledge.add_document(source_path, text)
        if not self._embeddings.available:
            return count

        with self._db._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, text FROM knowledge_chunks
                WHERE source_path = ?
                ORDER BY chunk_index
                """,
                (source_path,),
            ).fetchall()

        for row in rows:
            vector = await self._embeddings.embed(row["text"])
            if vector:
                self._db.store_embedding("knowledge", int(row["id"]), vector)

        return count

    def retrieve_skills_for_query(self, query: str, skills: list[Skill]) -> list[Skill]:
        return retrieve_skills(query, skills, top_k=self._skill_top_k)

    def context_for_prompt(
        self,
        query: str,
        memories: list[PersonalMemory],
        knowledge_chunks: list,
        skills: list[Skill],
    ) -> str:
        sections: list[str] = []

        if memories:
            lines = ["Relevant memories:"]
            for m in memories:
                lines.append(f"- [{m.category}] {m.content}")
            sections.append("\n".join(lines))

        if knowledge_chunks:
            lines = ["Knowledge base snippets:"]
            for chunk in knowledge_chunks[:3]:
                preview = chunk.text[:400].replace("\n", " ")
                lines.append(f"- {chunk.source_path}: {preview}")
            sections.append("\n".join(lines))

        if skills:
            lines = ["Relevant skills for this request:"]
            for skill in skills:
                first_line = skill.content.splitlines()[0] if skill.content else skill.name
                lines.append(f"- {skill.name}: {first_line}")
            sections.append("\n".join(lines))

        return "\n\n".join(sections)
