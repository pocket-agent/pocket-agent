from pocket_agent.config.models import PathsConfig
from pocket_agent.memory.service import MemoryService
from pocket_agent.tools.communication.telegram import send_telegram
from pocket_agent.tools.files.docx_edit import modify_docx
from pocket_agent.tools.files.excel import analyze_excel, modify_excel
from pocket_agent.tools.files.nas import index_files, list_nas_files, search_files
from pocket_agent.tools.files.pdf import extract_pdf_text
from pocket_agent.tools.files.pdf_edit import modify_pdf
from pocket_agent.tools.files.read import read_file
from pocket_agent.tools.web.search import web_search
from pocket_agent.tools.memory.tools import (
    index_knowledge,
    recall_memory,
    remember_memory,
    search_knowledge,
)
from pocket_agent.tools.registry import ToolRegistry


def build_tool_registry(
    paths: PathsConfig,
    bot=None,
    memory: MemoryService | None = None,
) -> ToolRegistry:
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

    return registry
