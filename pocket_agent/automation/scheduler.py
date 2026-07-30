"""Background reminder delivery."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable

import httpx

from pocket_agent.automation.reminders import ReminderStore

logger = logging.getLogger(__name__)

NotifyFn = Callable[[dict], Awaitable[None]]


class ReminderScheduler:
    def __init__(
        self,
        store: ReminderStore,
        notify: NotifyFn,
        poll_seconds: float = 30.0,
    ) -> None:
        self._store = store
        self._notify = notify
        self._poll_seconds = poll_seconds
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._loop(), name="reminder-scheduler")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None

    async def _loop(self) -> None:
        while True:
            try:
                for row in self._store.due():
                    await self._notify(row)
                    self._store.mark_sent(row["id"])
            except Exception:
                logger.exception("reminder scheduler tick failed")
            await asyncio.sleep(self._poll_seconds)


async def telegram_notify(
    token: str,
    reminder: dict,
) -> None:
    chat_id = reminder.get("chat_id")
    if not token or not chat_id:
        logger.info("REMINDER (no Telegram chat_id): %s", reminder.get("message"))
        return

    text = f"⏰ Reminder: {reminder.get('message', '')}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient(timeout=15.0) as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})
