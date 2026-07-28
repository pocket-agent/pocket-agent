from pocket_agent.config.models import PathsConfig
from pocket_agent.tools.communication.telegram import send_telegram
from pocket_agent.tools.files.nas import list_nas_files, search_files
from pocket_agent.tools.registry import ToolRegistry


def build_tool_registry(paths: PathsConfig, bot=None) -> ToolRegistry:
    registry = ToolRegistry()

    async def _list_nas(location: str | None = None, limit: int = 50):
        return await list_nas_files(paths, location=location, limit=limit)

    async def _search(query: str, location: str | None = None, limit: int = 25):
        return await search_files(paths, query=query, location=location, limit=limit)

    async def _send_telegram(chat_id: int, text: str):
        if bot is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Telegram bot not initialized")
        return await send_telegram(bot, chat_id, text, paths.logs_dir)

    registry.register("list_nas_files", _list_nas)
    registry.register("search_files", _search)
    registry.register("send_telegram", _send_telegram)

    return registry
