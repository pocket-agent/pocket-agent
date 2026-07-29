from pathlib import Path

from docx import Document

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.files.paths import resolve_read_path

MAX_READ_CHARS = 8000


async def read_file(
    paths: PathsConfig,
    file_path: str,
    max_chars: int = MAX_READ_CHARS,
) -> ToolResult:
    """Read supported files: PDF, TXT, DOCX, XLSX (summary). See TOOLS_SPEC read_file()."""
    resolved = resolve_read_path(paths, file_path)
    if isinstance(resolved, ToolResult):
        log_action(
            paths.logs_dir,
            "read_file",
            {"file_path": file_path},
            success=False,
            error=resolved.error,
        )
        return resolved

    path = resolved
    suffix = path.suffix.lower()

    try:
        if suffix == ".txt" or suffix == ".md":
            text = path.read_text(encoding="utf-8", errors="replace")
            content_type = "text"
        elif suffix == ".docx":
            doc = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
            content_type = "docx"
        elif suffix == ".pdf":
            from pocket_agent.tools.files.pdf import extract_pdf_text

            pdf_result = await extract_pdf_text(paths, str(path), max_chars=max_chars)
            if not pdf_result.success:
                return pdf_result
            text = pdf_result.data.get("text", "")
            content_type = "pdf"
        elif suffix in {".xlsx", ".xlsm"}:
            from pocket_agent.tools.files.excel import analyze_excel

            excel_result = await analyze_excel(paths, str(path))
            if not excel_result.success:
                return excel_result
            sheets = excel_result.data.get("sheets", [])
            lines = [f"Workbook: {path.name}", f"Sheet count: {len(sheets)}"]
            for sheet in sheets[:5]:
                lines.append(
                    f"- {sheet['name']}: {sheet['rows']} rows x {sheet['columns']} cols"
                )
            text = "\n".join(lines)
            content_type = "xlsx_summary"
        else:
            return ToolResult(
                success=False,
                error=f"Unsupported file type: {suffix or 'unknown'}",
            )

        truncated = len(text) > max_chars
        if truncated:
            text = text[:max_chars]

        log_action(
            paths.logs_dir,
            "read_file",
            {"file_path": str(path), "content_type": content_type, "truncated": truncated},
        )
        return ToolResult(
            success=True,
            data={
                "path": str(path),
                "content_type": content_type,
                "text": text,
                "truncated": truncated,
            },
        )
    except OSError as exc:
        log_action(
            paths.logs_dir,
            "read_file",
            {"file_path": str(path)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))
