import fitz

from pocket_agent.config.models import PathsConfig
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.files.paths import resolve_read_path
from pocket_agent.tools.files.safety import finalize_safe_edit, prepare_safe_edit
from pocket_agent.tools.files.validators import validate_pdf


async def modify_pdf(
    paths: PathsConfig,
    file_path: str,
    text: str,
    action: str = "add_page",
) -> ToolResult:
    """Add a new page with text (safe edit pipeline). See TOOLS_SPEC modify_pdf()."""
    if action != "add_page":
        return ToolResult(success=False, error=f"Unsupported PDF action: {action}")

    resolved = resolve_read_path(paths, file_path)
    if isinstance(resolved, ToolResult):
        log_action(
            paths.logs_dir,
            "modify_pdf",
            {"file_path": file_path},
            success=False,
            error=resolved.error,
        )
        return resolved

    path = resolved
    if path.suffix.lower() != ".pdf":
        return ToolResult(success=False, error="File is not a PDF")

    session = prepare_safe_edit(paths, path, "modify_pdf")
    if isinstance(session, ToolResult):
        return session

    try:
        with fitz.open(session.working_path) as doc:
            page = doc.new_page()
            page.insert_text((72, 72), text)
            doc.save(session.working_path)
    except Exception as exc:
        log_action(
            paths.logs_dir,
            "modify_pdf",
            {"file_path": str(path)},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))

    result = finalize_safe_edit(paths, session, validate_pdf, "modify_pdf")
    if result.success:
        result.data["action"] = action
        result.data["text_length"] = len(text)
    return result
