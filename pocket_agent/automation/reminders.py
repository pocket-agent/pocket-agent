"""Persisted reminders fired by the background scheduler."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _parse_when(when: str) -> datetime:
    raw = (when or "").strip()
    if not raw:
        raise ValueError("when is required (ISO-8601 datetime)")

    normalized = raw.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        raise ValueError("when must be ISO-8601, e.g. 2026-07-30T18:00:00+02:00") from None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


class ReminderStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> list[dict[str, Any]]:
        if not self._path.is_file():
            return []
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("reminder store read failed: %s", exc)
        return []

    def _save(self, rows: list[dict[str, Any]]) -> None:
        self._path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def add(
        self,
        message: str,
        when: str,
        user_key: str,
        chat_id: int | None = None,
    ) -> dict[str, Any]:
        text = (message or "").strip()
        if not text:
            raise ValueError("message is required")

        at = _parse_when(when)
        now = datetime.now(UTC)
        if at <= now:
            raise ValueError("when must be in the future")

        row = {
            "id": str(uuid.uuid4()),
            "message": text,
            "when": at.isoformat(),
            "user_key": user_key,
            "chat_id": chat_id,
            "status": "pending",
            "created_at": now.isoformat(),
        }
        rows = self._load()
        rows.append(row)
        self._save(rows)
        return row

    def list_pending(self, user_key: str | None = None) -> list[dict[str, Any]]:
        rows = self._load()
        pending = [r for r in rows if r.get("status") == "pending"]
        if user_key:
            pending = [r for r in pending if r.get("user_key") == user_key]
        pending.sort(key=lambda r: r.get("when", ""))
        return pending

    def cancel(self, task_id: str, user_key: str | None = None) -> bool:
        rows = self._load()
        tid = (task_id or "").strip()
        found = False
        for row in rows:
            rid = str(row.get("id", ""))
            if rid != tid and not (len(tid) >= 8 and rid.startswith(tid)):
                continue
            if user_key and row.get("user_key") != user_key:
                continue
            if row.get("status") != "pending":
                continue
            row["status"] = "cancelled"
            found = True
        if found:
            self._save(rows)
        return found

    def due(self) -> list[dict[str, Any]]:
        now = datetime.now(UTC)
        rows = self._load()
        due: list[dict[str, Any]] = []
        for row in rows:
            if row.get("status") != "pending":
                continue
            try:
                at = datetime.fromisoformat(str(row["when"]).replace("Z", "+00:00"))
                if at.tzinfo is None:
                    at = at.replace(tzinfo=UTC)
                at = at.astimezone(UTC)
            except ValueError:
                continue
            if at <= now:
                due.append(row)
        return due

    def mark_sent(self, task_id: str) -> None:
        rows = self._load()
        for row in rows:
            if row.get("id") == task_id:
                row["status"] = "sent"
                row["sent_at"] = datetime.now(UTC).isoformat()
        self._save(rows)
