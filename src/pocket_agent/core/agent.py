import re

from pocket_agent.core.skill_loader import Skill
from pocket_agent.llm.router import LlmRouter
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.registry import ToolRegistry

TELEGRAM_MAX_MESSAGE = 4000


class AgentCore:
    def __init__(
        self,
        llm_router: LlmRouter,
        tools: ToolRegistry,
        skills: list[Skill],
        system_prompt: str,
        logs_dir,
    ) -> None:
        self._llm = llm_router
        self._tools = tools
        self._skills = skills
        self._system_prompt = system_prompt
        self._logs_dir = logs_dir

    async def handle_message(self, user_text: str, chat_id: int | None = None) -> str:
        log_action(
            self._logs_dir,
            "user_message",
            {"text": user_text, "chat_id": chat_id},
        )

        tool_command = self._try_tool_command(user_text)
        if tool_command:
            result = await self._tools.run(**tool_command)
            if result.success:
                return self._truncate(self._format_tool_result(tool_command["name"], result.data))
            return f"Could not complete request: {result.error}"

        skills_summary = self._skills_summary()
        provider = self._llm.get("reasoning")
        prompt = (
            f"User message: {user_text}\n\n"
            f"Available skills:\n{skills_summary}\n\n"
            "Commands: /index, /nas, /search, /read, /pdf, /excel, "
            "/edit_excel, /edit_word, /edit_pdf, /help"
        )

        response = await provider.complete(prompt, system=self._system_prompt)
        log_action(
            self._logs_dir,
            "llm_response",
            {"provider": response.provider, "model": response.model},
        )
        return self._truncate(response.text.strip())

    def _truncate(self, text: str) -> str:
        if len(text) <= TELEGRAM_MAX_MESSAGE:
            return text
        return text[:TELEGRAM_MAX_MESSAGE - 20] + "\n… (truncated)"

    def _skills_summary(self) -> str:
        if not self._skills:
            return "No skills loaded."
        return "\n".join(f"- {s.name}: {s.content.splitlines()[0]}" for s in self._skills)

    def _try_tool_command(self, text: str) -> dict | None:
        stripped = text.strip()
        lower = stripped.lower()

        if lower == "/nas":
            return {"name": "list_nas_files", "location": None}

        if lower == "/index":
            return {"name": "index_files"}

        patterns: list[tuple[str, str, str]] = [
            (r"^/search\s+(.+)$", "search_files", "query"),
            (r"^/read\s+(.+)$", "read_file", "file_path"),
            (r"^/pdf\s+(.+)$", "extract_pdf_text", "file_path"),
            (r"^/excel\s+(.+)$", "analyze_excel", "file_path"),
        ]
        for pattern, tool_name, arg_name in patterns:
            match = re.match(pattern, stripped, re.IGNORECASE)
            if match:
                return {"name": tool_name, arg_name: match.group(1).strip()}

        edit_excel = re.match(
            r"^/edit_excel\s+(.+?)\s+([^\s]+)\s+([A-Za-z]+\d+)=(.+)$",
            stripped,
            re.IGNORECASE,
        )
        if edit_excel:
            return {
                "name": "modify_excel",
                "file_path": edit_excel.group(1).strip(),
                "sheet_name": edit_excel.group(2).strip(),
                "cell": edit_excel.group(3).strip().upper(),
                "value": edit_excel.group(4).strip(),
            }

        edit_word = re.match(
            r"^/edit_word\s+(.+?)\s+(append|replace_last)\s+(.+)$",
            stripped,
            re.IGNORECASE | re.DOTALL,
        )
        if edit_word:
            return {
                "name": "modify_docx",
                "file_path": edit_word.group(1).strip(),
                "action": edit_word.group(2).strip().lower(),
                "text": edit_word.group(3).strip(),
            }

        edit_pdf = re.match(
            r"^/edit_pdf\s+(.+?)\s+add_page\s+(.+)$",
            stripped,
            re.IGNORECASE | re.DOTALL,
        )
        if edit_pdf:
            return {
                "name": "modify_pdf",
                "file_path": edit_pdf.group(1).strip(),
                "action": "add_page",
                "text": edit_pdf.group(2).strip(),
            }

        return None

    def _format_tool_result(self, tool_name: str, data: dict) -> str:
        if tool_name == "list_nas_files":
            files = data.get("files", [])
            if not files:
                return f"No files found under {data.get('root', 'NAS')}."
            lines = [f"Files under {data.get('root')}:"]
            for f in files[:20]:
                lines.append(f"• {f['name']} ({f['size_bytes']} bytes)")
            return "\n".join(lines)

        if tool_name == "index_files":
            return (
                f"Indexed {data.get('indexed_count', 0)} files.\n"
                f"Database: {data.get('db_path')}"
            )

        if tool_name == "search_files":
            matches = data.get("matches", [])
            source = data.get("source", "unknown")
            if not matches:
                return f"No matches for '{data.get('query')}' (source: {source})."
            lines = [f"Matches for '{data.get('query')}' ({source}):"]
            for m in matches[:20]:
                ext = m.get("extension", "")
                suffix = f" [{ext}]" if ext else ""
                lines.append(f"• {m.get('path', m.get('name'))}{suffix}")
            return "\n".join(lines)

        if tool_name == "read_file":
            text = data.get("text", "")
            header = f"File: {data.get('path')} ({data.get('content_type')})"
            if data.get("truncated"):
                header += " [truncated]"
            return f"{header}\n\n{text}"

        if tool_name == "extract_pdf_text":
            header = f"PDF: {data.get('path')} ({data.get('page_count')} pages)"
            if data.get("truncated"):
                header += " [truncated]"
            return f"{header}\n\n{data.get('text', '')}"

        if tool_name == "analyze_excel":
            lines = [f"Workbook: {data.get('path')}", f"Sheets: {data.get('sheet_count')}"]
            for sheet in data.get("sheets", [])[:5]:
                lines.append(f"\n## {sheet['name']} ({sheet['rows']} x {sheet['columns']})")
                for row in sheet.get("sample", [])[:3]:
                    lines.append(" | ".join(row))
            return "\n".join(lines)

        if tool_name in {"modify_excel", "modify_pdf", "modify_docx"}:
            lines = [
                f"Updated: {data.get('path')}",
                f"Backup: {data.get('backup_path')}",
            ]
            if tool_name == "modify_excel":
                lines.append(f"Cell {data.get('sheet')}!{data.get('cell')} = {data.get('value')}")
            elif tool_name == "modify_docx":
                lines.append(f"Action: {data.get('action')}")
            elif tool_name == "modify_pdf":
                lines.append(f"Action: {data.get('action')} (+{data.get('text_length')} chars)")
            return "\n".join(lines)

        return str(data)
