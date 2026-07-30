"""Agent-facing reminder tools."""

from __future__ import annotations

from pocket_agent.automation.reminders import ReminderStore
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult


async def schedule_reminder(
    store: ReminderStore,
    logs_dir,
    message: str,
    when: str,
    user_key: str,
    chat_id: int | None = None,
) -> ToolResult:
    try:
        row = store.add(message, when, user_key=user_key, chat_id=chat_id)
    except ValueError as exc:
        return ToolResult(success=False, error=str(exc))

    log_action(
        logs_dir,
        "schedule_reminder",
        {"id": row["id"], "when": row["when"], "user_key": user_key},
    )
    return ToolResult(
        success=True,
        data={
            "id": row["id"],
            "message": row["message"],
            "when": row["when"],
            "summary": f"Reminder scheduled for {row['when']}: {row['message']}",
        },
    )


async def list_scheduled_tasks(
    store: ReminderStore,
    user_key: str | None = None,
) -> ToolResult:
    rows = store.list_pending(user_key=user_key)
    return ToolResult(
        success=True,
        data={
            "count": len(rows),
            "tasks": rows,
            "summary": "\n".join(
                f"- {r['id'][:8]}… at {r['when']}: {r['message']}" for r in rows[:20]
            )
            or "No pending reminders.",
        },
    )


async def cancel_task(
    store: ReminderStore,
    task_id: str,
    user_key: str | None = None,
) -> ToolResult:
    tid = (task_id or "").strip()
    if not tid:
        return ToolResult(success=False, error="task_id is required")

    ok = store.cancel(tid, user_key=user_key)
    if not ok:
        return ToolResult(success=False, error="Reminder not found or already completed")
    return ToolResult(success=True, data={"task_id": tid, "summary": "Reminder cancelled."})
