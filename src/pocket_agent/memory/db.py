import json
import math
import re
import sqlite3
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS personal_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL DEFAULT 'preference',
    content TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_path TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    entity_id INTEGER NOT NULL,
    vector_json TEXT NOT NULL,
    UNIQUE(entity_type, entity_id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content,
    category,
    content='personal_memories',
    content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
    text,
    source_path,
    content='knowledge_chunks',
    content_rowid='id'
);
"""

_FTS_TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON personal_memories BEGIN
    INSERT INTO memories_fts(rowid, content, category) VALUES (new.id, new.content, new.category);
END;
CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON personal_memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content, category)
        VALUES ('delete', old.id, old.content, old.category);
END;
CREATE TRIGGER IF NOT EXISTS knowledge_ai AFTER INSERT ON knowledge_chunks BEGIN
    INSERT INTO knowledge_fts(rowid, text, source_path) VALUES (new.id, new.text, new.source_path);
END;
CREATE TRIGGER IF NOT EXISTS knowledge_ad AFTER DELETE ON knowledge_chunks BEGIN
    INSERT INTO knowledge_fts(knowledge_fts, rowid, text, source_path)
        VALUES ('delete', old.id, old.text, old.source_path);
END;
"""


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class MemoryDatabase:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)
            conn.executescript(_FTS_TRIGGERS)

    def store_embedding(self, entity_type: str, entity_id: int, vector: list[float]) -> None:
        payload = json.dumps(vector)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO embeddings (entity_type, entity_id, vector_json)
                VALUES (?, ?, ?)
                ON CONFLICT(entity_type, entity_id) DO UPDATE SET vector_json = excluded.vector_json
                """,
                (entity_type, entity_id, payload),
            )

    def vector_search(
        self,
        query_vector: list[float],
        entity_type: str,
        limit: int = 5,
    ) -> list[tuple[int, float]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT entity_id, vector_json FROM embeddings WHERE entity_type = ?",
                (entity_type,),
            ).fetchall()

        scored: list[tuple[int, float]] = []
        for row in rows:
            vector = json.loads(row["vector_json"])
            score = cosine_similarity(query_vector, vector)
            scored.append((int(row["entity_id"]), score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]


SECRET_PATTERNS = [
    re.compile(r"password\s*[:=]", re.I),
    re.compile(r"api[_-]?key", re.I),
    re.compile(r"secret\s*[:=]", re.I),
    re.compile(r"token\s*[:=]", re.I),
    re.compile(r"BEGIN (RSA |OPENSSH )?PRIVATE KEY", re.I),
]


def looks_like_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)
