import sqlite3
import time
from dataclasses import dataclass

from pocket_agent.memory.db import MemoryDatabase
from pocket_agent.memory.fts import fts_query


@dataclass
class KnowledgeChunk:
    id: int
    source_path: str
    chunk_index: int
    text: str
    created_at: float


def chunk_text(text: str, chunk_size: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size
    return chunks


class KnowledgeBase:
    def __init__(self, db: MemoryDatabase, chunk_size: int = 1000) -> None:
        self._db = db
        self._chunk_size = chunk_size

    def clear(self) -> None:
        with self._db._connect() as conn:
            conn.execute("DELETE FROM knowledge_chunks")
            conn.execute("DELETE FROM embeddings WHERE entity_type = 'knowledge'")

    def add_document(self, source_path: str, text: str) -> int:
        chunks = chunk_text(text, self._chunk_size)
        created_at = time.time()
        count = 0
        with self._db._connect() as conn:
            for index, chunk in enumerate(chunks):
                conn.execute(
                    """
                    INSERT INTO knowledge_chunks (source_path, chunk_index, text, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (source_path, index, chunk, created_at),
                )
                count += 1
        return count

    def search_fts(self, query: str, limit: int = 5) -> list[KnowledgeChunk]:
        with self._db._connect() as conn:
            try:
                rows = conn.execute(
                    """
                    SELECT k.id, k.source_path, k.chunk_index, k.text, k.created_at
                    FROM knowledge_fts f
                    JOIN knowledge_chunks k ON k.id = f.rowid
                    WHERE knowledge_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (fts_query(query), limit),
                ).fetchall()
            except sqlite3.OperationalError:
                return []

        return [
            KnowledgeChunk(
                id=row["id"],
                source_path=row["source_path"],
                chunk_index=row["chunk_index"],
                text=row["text"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_by_ids(self, ids: list[int]) -> list[KnowledgeChunk]:
        if not ids:
            return []
        placeholders = ",".join("?" for _ in ids)
        with self._db._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT id, source_path, chunk_index, text, created_at
                FROM knowledge_chunks WHERE id IN ({placeholders})
                """,
                ids,
            ).fetchall()
        return [
            KnowledgeChunk(
                id=row["id"],
                source_path=row["source_path"],
                chunk_index=row["chunk_index"],
                text=row["text"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def count(self) -> int:
        with self._db._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM knowledge_chunks").fetchone()
            return int(row["c"])
