from pathlib import Path
from typing import Any

from pocket_agent.automation.reminders import ReminderStore
from pocket_agent.automation.scripts import run_allowed_script
from pocket_agent.config.models import AppSettings, PathsConfig
from pocket_agent.memory.service import MemoryService
from pocket_agent.tools.automation.reminders import (
    cancel_task,
    list_scheduled_tasks,
    schedule_reminder,
)
from pocket_agent.tools.calendar.ics_calendar import calendar_events
from pocket_agent.tools.communication.telegram import send_telegram
from pocket_agent.tools.files.docx_edit import modify_docx
from pocket_agent.tools.files.excel import analyze_excel, modify_excel
from pocket_agent.tools.files.nas import index_files, list_nas_files, search_files
from pocket_agent.tools.files.pdf import extract_pdf_text
from pocket_agent.tools.files.pdf_edit import modify_pdf
from pocket_agent.tools.files.read import read_file
from pocket_agent.tools.memory.tools import (
    index_knowledge,
    recall_memory,
    remember_memory,
    search_knowledge,
)
from pocket_agent.tools.registry import ToolRegistry
from pocket_agent.tools.util.currency import exchange_rate
from pocket_agent.tools.util.timezone import timezone_now
from pocket_agent.tools.util.units import unit_convert
from pocket_agent.tools.web.fetch import fetch_url
from pocket_agent.tools.web.search import web_search
from pocket_agent.tools.web.weather import current_weather


def build_tool_registry(
    paths: PathsConfig,
    memory: MemoryService | None = None,
    env: AppSettings | None = None,
    project_root: Path | None = None,
    raw_settings: dict[str, Any] | None = None,
    bot=None,
) -> ToolRegistry:
    registry = ToolRegistry()
    settings = raw_settings or {}
    root = project_root or paths.project_root
    reminder_store = ReminderStore(paths.queue_dir / "reminders.json")

    async def _list_nas(location: str | None = None, limit: int = 50):
        return await list_nas_files(paths, location=location, limit=limit)

    async def _index(max_depth: int = 12):
        return await index_files(paths, max_depth=max_depth)

    async def _search(
        query: str,
        location: str | None = None,
        extension: str | None = None,
        limit: int = 25,
    ):
        return await search_files(
            paths,
            query=query,
            location=location,
            extension=extension,
            limit=limit,
        )

    async def _read(file_path: str, max_chars: int = 8000):
        return await read_file(paths, file_path=file_path, max_chars=max_chars)

    async def _extract_pdf(file_path: str, max_chars: int = 8000):
        return await extract_pdf_text(paths, file_path=file_path, max_chars=max_chars)

    async def _analyze_excel(file_path: str):
        return await analyze_excel(paths, file_path=file_path)

    async def _modify_excel(file_path: str, sheet_name: str, cell: str, value: str):
        return await modify_excel(
            paths,
            file_path=file_path,
            sheet_name=sheet_name,
            cell=cell,
            value=value,
        )

    async def _modify_pdf(file_path: str, text: str, action: str = "add_page"):
        return await modify_pdf(paths, file_path=file_path, text=text, action=action)

    async def _modify_docx(file_path: str, text: str, action: str = "append"):
        return await modify_docx(paths, file_path=file_path, text=text, action=action)

    async def _remember(user_id: int, content: str, category: str = "preference"):
        if memory is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Memory service not initialized")
        return await remember_memory(memory, paths, user_id, content, category=category)

    async def _recall(query: str, user_id: int | None = None, limit: int = 5):
        if memory is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Memory service not initialized")
        return await recall_memory(memory, paths, query, user_id=user_id, limit=limit)

    async def _search_knowledge(query: str, limit: int = 5):
        if memory is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Memory service not initialized")
        return await search_knowledge(memory, paths, query, limit=limit)

    async def _index_knowledge(max_files: int = 100):
        if memory is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Memory service not initialized")
        return await index_knowledge(memory, paths, max_files=max_files)

    async def _send_telegram(chat_id: int, text: str):
        if bot is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Telegram bot not initialized")
        return await send_telegram(bot, chat_id, text, paths.logs_dir)

    async def _web_search(query: str, max_results: int = 5):
        return await web_search(query=query, max_results=max_results)

    async def _current_weather(location: str):
        return await current_weather(location=location)

    async def _fetch_url(url: str, max_chars: int = 12000):
        return await fetch_url(url=url, max_chars=max_chars)

    async def _timezone_now(location: str):
        return await timezone_now(location=location)

    async def _exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0):
        return await exchange_rate(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
        )

    async def _unit_convert(value: float, from_unit: str, to_unit: str):
        return await unit_convert(value=value, from_unit=from_unit, to_unit=to_unit)

    async def _calendar_events(days_ahead: int = 7):
        ics = (env.calendar_ics_url if env else "") or ""
        return await calendar_events(ics_url=ics, days_ahead=days_ahead)

    async def _schedule_reminder(
        message: str,
        when: str,
        user_key: str = "local",
        chat_id: int | None = None,
    ):
        return await schedule_reminder(
            reminder_store,
            paths.logs_dir,
            message=message,
            when=when,
            user_key=user_key,
            chat_id=chat_id,
        )

    async def _list_scheduled_tasks(user_key: str | None = None):
        return await list_scheduled_tasks(reminder_store, user_key=user_key)

    async def _cancel_task(task_id: str, user_key: str | None = None):
        return await cancel_task(reminder_store, task_id=task_id, user_key=user_key)

    async def _run_allowed_script(script_name: str, timeout_seconds: int = 120):
        return await run_allowed_script(
            root,
            settings,
            script_name=script_name,
            timeout_seconds=timeout_seconds,
        )

    registry.register("list_nas_files", _list_nas)
    registry.register("index_files", _index)
    registry.register("search_files", _search)
    registry.register("read_file", _read)
    registry.register("extract_pdf_text", _extract_pdf)
    registry.register("analyze_excel", _analyze_excel)
    registry.register("modify_excel", _modify_excel)
    registry.register("modify_pdf", _modify_pdf)
    registry.register("modify_docx", _modify_docx)
    registry.register("remember_memory", _remember)
    registry.register("recall_memory", _recall)
    registry.register("search_knowledge", _search_knowledge)
    registry.register("index_knowledge", _index_knowledge)
    registry.register("send_telegram", _send_telegram)
    registry.register("web_search", _web_search)
    registry.register("current_weather", _current_weather)
    registry.register("fetch_url", _fetch_url)
    registry.register("timezone_now", _timezone_now)
    registry.register("exchange_rate", _exchange_rate)
    registry.register("unit_convert", _unit_convert)
    registry.register("calendar_events", _calendar_events)
    registry.register("schedule_reminder", _schedule_reminder)
    registry.register("list_scheduled_tasks", _list_scheduled_tasks)
    registry.register("cancel_task", _cancel_task)
    registry.register("run_allowed_script", _run_allowed_script)

    return registry
