import sqlite3
from pathlib import Path

from pocket_agent.indexing.models import FileRecord

_SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    path TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    extension TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    modified_at REAL NOT NULL,
    parent TEXT NOT NULL,
    indexed_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_files_name ON files(name);
CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
"""


class FileIndexStore:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM files")

    def upsert_batch(self, records: list[FileRecord], indexed_at: float) -> None:
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO files (path, name, extension, size_bytes, modified_at, parent, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    name=excluded.name,
                    extension=excluded.extension,
                    size_bytes=excluded.size_bytes,
                    modified_at=excluded.modified_at,
                    parent=excluded.parent,
                    indexed_at=excluded.indexed_at
                """,
                [
                    (
                        r.path,
                        r.name,
                        r.extension,
                        r.size_bytes,
                        r.modified_at,
                        r.parent,
                        indexed_at,
                    )
                    for r in records
                ],
            )

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS c FROM files").fetchone()
            return int(row["c"])

    def search(
        self,
        query: str,
        extension: str | None = None,
        limit: int = 25,
    ) -> list[FileRecord]:
        query_lower = query.lower().strip()
        sql = """
            SELECT path, name, extension, size_bytes, modified_at, parent
            FROM files
            WHERE (LOWER(name) LIKE ? OR LOWER(path) LIKE ?)
        """
        params: list[str | int] = [f"%{query_lower}%", f"%{query_lower}%"]

        if extension:
            sql += " AND extension = ?"
            params.append(extension.lower().lstrip("."))

        sql += " ORDER BY modified_at DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [
            FileRecord(
                path=row["path"],
                name=row["name"],
                extension=row["extension"],
                size_bytes=row["size_bytes"],
                modified_at=row["modified_at"],
                parent=row["parent"],
            )
            for row in rows
        ]
