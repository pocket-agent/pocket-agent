from pocket_agent.config.models import PathsConfig
from pocket_agent.tools.communication.telegram import send_telegram
from pocket_agent.tools.files.excel import analyze_excel
from pocket_agent.tools.files.nas import index_files, list_nas_files, search_files
from pocket_agent.tools.files.pdf import extract_pdf_text
from pocket_agent.tools.files.read import read_file
from pocket_agent.tools.registry import ToolRegistry


def build_tool_registry(paths: PathsConfig, bot=None) -> ToolRegistry:
    registry = ToolRegistry()

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

    async def _send_telegram(chat_id: int, text: str):
        if bot is None:
            from pocket_agent.tools.base import ToolResult

            return ToolResult(success=False, error="Telegram bot not initialized")
        return await send_telegram(bot, chat_id, text, paths.logs_dir)

    registry.register("list_nas_files", _list_nas)
    registry.register("index_files", _index)
    registry.register("search_files", _search)
    registry.register("read_file", _read)
    registry.register("extract_pdf_text", _extract_pdf)
    registry.register("analyze_excel", _analyze_excel)
    registry.register("send_telegram", _send_telegram)

    return registry
