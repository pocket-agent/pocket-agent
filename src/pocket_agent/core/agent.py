import re

from pocket_agent.core.skill_loader import Skill, load_skills, load_system_prompt
from pocket_agent.llm.router import LlmRouter
from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.registry import ToolRegistry


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

        nas_command = self._try_nas_command(user_text)
        if nas_command:
            result = await self._tools.run(**nas_command)
            if result.success:
                return self._format_tool_result(nas_command["name"], result.data)
            return f"Could not complete request: {result.error}"

        skills_summary = self._skills_summary()
        provider = self._llm.get("reasoning")
        prompt = (
            f"User message: {user_text}\n\n"
            f"Available skills:\n{skills_summary}\n\n"
            "Respond helpfully. If the user asks to list or search NAS files, "
            "tell them to use commands: /nas or /search <query>."
        )

        response = await provider.complete(prompt, system=self._system_prompt)
        log_action(
            self._logs_dir,
            "llm_response",
            {"provider": response.provider, "model": response.model},
        )
        return response.text.strip()

    def _skills_summary(self) -> str:
        if not self._skills:
            return "No skills loaded."
        return "\n".join(f"- {s.name}: {s.content.splitlines()[0]}" for s in self._skills)

    def _try_nas_command(self, text: str) -> dict | None:
        stripped = text.strip()
        if stripped.lower() == "/nas":
            return {"name": "list_nas_files", "location": None}
        match = re.match(r"^/search\s+(.+)$", stripped, re.IGNORECASE)
        if match:
            return {"name": "search_files", "query": match.group(1).strip()}
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

        if tool_name == "search_files":
            matches = data.get("matches", [])
            if not matches:
                return f"No matches for '{data.get('query')}'."
            lines = [f"Matches for '{data.get('query')}':"]
            for m in matches[:20]:
                lines.append(f"• {m['path']}")
            return "\n".join(lines)

        return str(data)
