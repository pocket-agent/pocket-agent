import fitz

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.files.paths import resolve_read_path


async def extract_pdf_text(
    paths: PathsConfig,
    file_path: str,
    max_chars: int = 8000,
) -> ToolResult:
    """Extract text from a PDF. See TOOLS_SPEC extract_pdf_text()."""
    resolved = resolve_read_path(paths, file_path)
    if isinstance(resolved, ToolResult):
        log_action(
            paths.logs_dir,
            "extract_pdf_text",
            {"file_path": file_path},
            success=False,
            error=resolved.error,
        )
        return resolved

    path = resolved
    if path.suffix.lower() != ".pdf":
        return ToolResult(success=False, error="File is not a PDF")

    try:
        with fitz.open(path) as doc:
            pages: list[str] = []
            for page in doc:
                pages.append(page.get_text())
            text = "\n".join(pages).strip()
            page_count = doc.page_count

        truncated = len(text) > max_chars
        if truncated:
            text = text[:max_chars]

        log_action(
            paths.logs_dir,
            "extract_pdf_text",
            {"file_path": str(path), "page_count": page_count, "truncated": truncated},
        )
        return ToolResult(
            success=True,
            data={
                "path": str(path),
                "text": text,
                "page_count": page_count,
                "truncated": truncated,
            },
        )
    except Exception as exc:
        log_action(
            paths.logs_dir,
            "extract_pdf_text",
            {"file_path": str(path)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))
