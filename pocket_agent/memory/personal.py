import sqlite3
import time
from dataclasses import dataclass

from pocket_agent.memory.db import MemoryDatabase, looks_like_secret
from pocket_agent.memory.fts import fts_query


@dataclass
class PersonalMemory:
    id: int
    user_id: int
    category: str
    content: str
    created_at: float


class PersonalMemoryStore:
    def __init__(self, db: MemoryDatabase) -> None:
        self._db = db

    def add(self, user_id: int, content: str, category: str = "preference") -> PersonalMemory | str:
        text = content.strip()
        if not text:
            return "Memory content is empty"
        if looks_like_secret(text):
            return "Refusing to store content that looks like a secret"

        created_at = time.time()
        with self._db._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO personal_memories (user_id, category, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, category, text, created_at),
            )
            memory_id = int(cursor.lastrowid)

        return PersonalMemory(
            id=memory_id,
            user_id=user_id,
            category=category,
            content=text,
            created_at=created_at,
        )

    def search_fts(self, query: str, user_id: int | None = None, limit: int = 5) -> list[PersonalMemory]:
        sql = """
            SELECT m.id, m.user_id, m.category, m.content, m.created_at
            FROM memories_fts f
            JOIN personal_memories m ON m.id = f.rowid
            WHERE memories_fts MATCH ?
        """
        params: list = [fts_query(query)]
        if user_id is not None:
            sql += " AND m.user_id = ?"
            params.append(user_id)
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)

        with self._db._connect() as conn:
            try:
                rows = conn.execute(sql, params).fetchall()
            except sqlite3.OperationalError:
                return []

        return [
            PersonalMemory(
                id=row["id"],
                user_id=row["user_id"],
                category=row["category"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_by_ids(self, ids: list[int]) -> list[PersonalMemory]:
        if not ids:
            return []
        placeholders = ",".join("?" for _ in ids)
        with self._db._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT id, user_id, category, content, created_at
                FROM personal_memories WHERE id IN ({placeholders})
                """,
                ids,
            ).fetchall()
        return [
            PersonalMemory(
                id=row["id"],
                user_id=row["user_id"],
                category=row["category"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def list_recent(self, user_id: int, limit: int = 10) -> list[PersonalMemory]:
        with self._db._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, user_id, category, content, created_at
                FROM personal_memories
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        return [
            PersonalMemory(
                id=row["id"],
                user_id=row["user_id"],
                category=row["category"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def count(self) -> int:
        with self._db._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM personal_memories").fetchone()
            return int(row["c"])

    def clear_all(self) -> int:
        with self._db._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM personal_memories").fetchone()
            deleted = int(row["c"])
            conn.execute("DELETE FROM embeddings WHERE entity_type = 'memory'")
            conn.execute("DELETE FROM personal_memories")
        return deleted
