from pathlib import Path

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.memory.service import MemoryService
from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.files.paths import resolve_read_path
from pocket_agent.tools.files.pdf import extract_pdf_text


TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}


async def remember_memory(
    memory: MemoryService,
    paths: PathsConfig,
    user_id: int,
    content: str,
    category: str = "preference",
) -> ToolResult:
    result = await memory.remember(user_id, content, category=category)
    if isinstance(result, str):
        log_action(
            paths.logs_dir,
            "remember_memory",
            {"user_id": user_id},
            success=False,
            error=result,
        )
        return ToolResult(success=False, error=result)

    log_action(
        paths.logs_dir,
        "remember_memory",
        {"user_id": user_id, "memory_id": result.id, "category": category},
    )
    return ToolResult(
        success=True,
        data={"id": result.id, "content": result.content, "category": result.category},
    )


async def recall_memory(
    memory: MemoryService,
    paths: PathsConfig,
    query: str,
    user_id: int | None = None,
    limit: int = 5,
) -> ToolResult:
    results = await memory.recall(query, user_id=user_id, limit=limit)
    log_action(
        paths.logs_dir,
        "recall_memory",
        {"query": query, "user_id": user_id, "count": len(results)},
    )
    return ToolResult(
        success=True,
        data={
            "query": query,
            "memories": [
                {"id": m.id, "category": m.category, "content": m.content} for m in results
            ],
        },
    )


async def search_knowledge(
    memory: MemoryService,
    paths: PathsConfig,
    query: str,
    limit: int = 5,
) -> ToolResult:
    chunks = await memory.search_knowledge(query, limit=limit)
    log_action(
        paths.logs_dir,
        "search_knowledge",
        {"query": query, "count": len(chunks)},
    )
    return ToolResult(
        success=True,
        data={
            "query": query,
            "results": [
                {
                    "source_path": c.source_path,
                    "chunk_index": c.chunk_index,
                    "text": c.text[:500],
                }
                for c in chunks
            ],
        },
    )


async def index_knowledge(
    memory: MemoryService,
    paths: PathsConfig,
    max_files: int = 100,
) -> ToolResult:
    """Index text from NAS files (.txt, .md, .pdf) into the knowledge base."""
    indexed_files = 0
    total_chunks = 0
    errors: list[str] = []

    memory.knowledge.clear()

    candidates: list[Path] = []
    for root in paths.allowed_read_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS.union({".pdf"}):
                candidates.append(path)
            if len(candidates) >= max_files:
                break

    for path in candidates[:max_files]:
        try:
            if path.suffix.lower() == ".pdf":
                pdf_result = await extract_pdf_text(paths, str(path), max_chars=20000)
                if not pdf_result.success:
                    errors.append(f"{path.name}: {pdf_result.error}")
                    continue
                text = pdf_result.data.get("text", "")
            else:
                text = path.read_text(encoding="utf-8", errors="replace")

            chunks = await memory.index_knowledge_chunk(str(path.resolve()), text)
            if chunks:
                indexed_files += 1
                total_chunks += chunks
        except OSError as exc:
            errors.append(f"{path.name}: {exc}")

    log_action(
        paths.logs_dir,
        "index_knowledge",
        {"indexed_files": indexed_files, "total_chunks": total_chunks, "errors": len(errors)},
    )
    return ToolResult(
        success=True,
        data={
            "indexed_files": indexed_files,
            "total_chunks": total_chunks,
            "errors": errors[:5],
            "embeddings": memory.embeddings_available,
        },
    )
