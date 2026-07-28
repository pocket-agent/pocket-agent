import re

from pocket_agent.core.skill_loader import Skill
from pocket_agent.llm.router import LlmRouter
from pocket_agent.logging.action_log import log_action
from pocket_agent.memory.service import MemoryService
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
        memory: MemoryService | None = None,
    ) -> None:
        self._llm = llm_router
        self._tools = tools
        self._skills = skills
        self._system_prompt = system_prompt
        self._logs_dir = logs_dir
        self._memory = memory

    async def handle_message(self, user_text: str, chat_id: int | None = None) -> str:
        return await self.handle_chat_message(user_text, chat_id=chat_id)

    async def handle_chat_message(
        self,
        user_text: str,
        *,
        history: list[dict] | None = None,
        chat_id: int | None = None,
    ) -> str:
        log_action(
            self._logs_dir,
            "user_message",
            {"text": user_text, "chat_id": chat_id},
        )

        tool_command = self._try_tool_command(user_text, chat_id=chat_id)
        if tool_command:
            result = await self._tools.run(**tool_command)
            if result.success:
                return self._truncate(self._format_tool_result(tool_command["name"], result.data))
            return f"Could not complete request: {result.error}"

        return await self._handle_llm_message(user_text, chat_id=chat_id, history=history or [])

    async def _handle_llm_message(
        self,
        user_text: str,
        chat_id: int | None = None,
        history: list[dict] | None = None,
    ) -> str:
        relevant_skills = self._skills
        memory_block = ""
        user_id = chat_id

        if self._memory:
            relevant_skills = self._memory.retrieve_skills_for_query(user_text, self._skills)
            memories = await self._memory.recall(user_text, user_id=user_id, limit=3)
            knowledge = await self._memory.search_knowledge(user_text, limit=3)
            memory_block = self._memory.context_for_prompt(
                user_text, memories, knowledge, relevant_skills
            )

        skills_summary = self._skills_summary(relevant_skills)
        provider = self._llm.get("reasoning")

        prompt_parts: list[str] = []
        if history:
            hist_lines: list[str] = []
            for item in history[-20:]:
                role = item.get("role", "user")
                content = (item.get("content") or "").strip()
                if content:
                    hist_lines.append(f"{role}: {content}")
            if hist_lines:
                prompt_parts.append("Conversation history:\n" + "\n".join(hist_lines))

        prompt_parts.append(f"User message: {user_text}")
        if memory_block:
            prompt_parts.append(memory_block)
        prompt_parts.append(f"Available skills:\n{skills_summary}")
        prompt_parts.append(
            "Commands: /remember, /recall, /kb, /kb_index, /index, /nas, /search, "
            "/read, /pdf, /excel, /edit_excel, /edit_word, /edit_pdf, /help"
        )
        prompt = "\n\n".join(prompt_parts)

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

    def _skills_summary(self, skills: list[Skill] | None = None) -> str:
        items = skills if skills is not None else self._skills
        if not items:
            return "No skills loaded."
        return "\n".join(f"- {s.name}: {s.content.splitlines()[0]}" for s in items)

    def _try_tool_command(self, text: str, chat_id: int | None = None) -> dict | None:
        stripped = text.strip()
        lower = stripped.lower()

        if lower == "/nas":
            return {"name": "list_nas_files", "location": None}

        if lower == "/index":
            return {"name": "index_files"}

        if lower == "/kb_index":
            return {"name": "index_knowledge"}

        remember = re.match(r"^/remember\s+(.+)$", stripped, re.IGNORECASE | re.DOTALL)
        if remember and chat_id is not None:
            return {
                "name": "remember_memory",
                "user_id": chat_id,
                "content": remember.group(1).strip(),
            }

        recall = re.match(r"^/recall\s+(.+)$", stripped, re.IGNORECASE | re.DOTALL)
        if recall:
            return {
                "name": "recall_memory",
                "query": recall.group(1).strip(),
                "user_id": chat_id,
            }

        kb = re.match(r"^/kb\s+(.+)$", stripped, re.IGNORECASE | re.DOTALL)
        if kb:
            return {"name": "search_knowledge", "query": kb.group(1).strip()}

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

        if tool_name == "index_knowledge":
            return (
                f"Knowledge base: {data.get('total_chunks', 0)} chunks "
                f"from {data.get('indexed_files', 0)} files.\n"
                f"Embeddings: {'yes' if data.get('embeddings') else 'FTS only'}"
            )

        if tool_name == "remember_memory":
            return f"Remembered [{data.get('category')}]: {data.get('content')}"

        if tool_name == "recall_memory":
            memories = data.get("memories", [])
            if not memories:
                return f"No memories for '{data.get('query')}'."
            lines = [f"Memories for '{data.get('query')}':"]
            for m in memories:
                lines.append(f"• [{m['category']}] {m['content']}")
            return "\n".join(lines)

        if tool_name == "search_knowledge":
            results = data.get("results", [])
            if not results:
                return f"No knowledge hits for '{data.get('query')}'."
            lines = [f"Knowledge for '{data.get('query')}':"]
            for r in results:
                lines.append(f"• {r['source_path']} (chunk {r['chunk_index']})")
                lines.append(f"  {r['text'][:200]}")
            return "\n".join(lines)

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
