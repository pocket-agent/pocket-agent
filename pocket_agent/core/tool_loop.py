"""Parse and run tool calls from LLM text responses."""

from __future__ import annotations

import json
import re
from collections.abc import Awaitable, Callable
from typing import Any

from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.catalog import AGENT_TOOL_SPECS

MAX_AGENT_STEPS = 6

ToolRunner = Callable[..., Awaitable[ToolResult]]

_FENCED_JSON_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)

_SUMMARY_TOOLS = frozenset(
    {
        "current_weather",
        "timezone_now",
        "exchange_rate",
        "unit_convert",
        "calendar_events",
        "schedule_reminder",
        "list_scheduled_tasks",
        "cancel_task",
        "fetch_url",
    }
)


def _parse_payload(raw: str) -> tuple[str, dict[str, Any]] | None:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    tool = payload.get("tool")
    args = payload.get("arguments") or {}
    if isinstance(tool, str) and tool in AGENT_TOOL_SPECS and isinstance(args, dict):
        return tool, args
    return None


def parse_tool_call(text: str) -> tuple[str, dict[str, Any]] | None:
    """Extract first tool call from model output."""
    stripped = text.strip()
    if not stripped:
        return None

    for match in _FENCED_JSON_RE.finditer(stripped):
        parsed = _parse_payload(match.group(1))
        if parsed:
            return parsed

    start = stripped.find("{")
    while start >= 0:
        try:
            payload, _end = json.JSONDecoder().raw_decode(stripped, start)
            if isinstance(payload, dict) and "tool" in payload:
                parsed = _parse_payload(json.dumps(payload))
                if parsed:
                    return parsed
        except json.JSONDecodeError:
            pass
        start = stripped.find("{", start + 1)

    return None


def format_tool_result(tool_name: str, result: ToolResult) -> str:
    if not result.success:
        return f"[{tool_name}] ERROR: {result.error or 'failed'}"
    data = result.data or {}
    if tool_name in _SUMMARY_TOOLS and data.get("summary"):
        return f"[{tool_name}] {data['summary']}"
    if tool_name == "web_search":
        lines = [f"[web_search] query={data.get('query')}"]
        if data.get("hint"):
            lines.append(str(data["hint"]))
        for i, row in enumerate(data.get("results") or [], 1):
            lines.append(
                f"{i}. {row.get('title', '')}\n   {row.get('url', '')}\n   {row.get('snippet', '')}"
            )
        if len(lines) == 1:
            lines.append("No results.")
        return "\n".join(lines)
    if tool_name == "recall_memory":
        memories = data.get("memories") or []
        if not memories:
            return f"[recall_memory] No memories for '{data.get('query')}'."
        lines = [f"[recall_memory] query={data.get('query')}"]
        for m in memories:
            lines.append(f"- [{m.get('category')}] {m.get('content')}")
        return "\n".join(lines)
    if tool_name == "search_knowledge":
        hits = data.get("results") or []
        if not hits:
            return f"[search_knowledge] No hits for '{data.get('query')}'."
        lines = [f"[search_knowledge] query={data.get('query')}"]
        for r in hits:
            lines.append(f"- {r.get('source_path')}: {str(r.get('text', ''))[:200]}")
        return "\n".join(lines)
    if tool_name == "remember_memory":
        return f"[remember_memory] Stored [{data.get('category')}]: {data.get('content')}"
    if tool_name == "fetch_url":
        text = str(data.get("text", ""))[:3500]
        header = f"[fetch_url] {data.get('url')}"
        if data.get("truncated"):
            header += " [truncated]"
        return f"{header}\n{text}"
    if tool_name == "run_allowed_script":
        return (
            f"[run_allowed_script] {data.get('script')} exit={data.get('exit_code')}\n"
            f"{data.get('stdout', '')[:2000]}"
        )
    return f"[{tool_name}] {json.dumps(data, ensure_ascii=False)[:4000]}"


async def run_agent_tool_loop(
    tool_runner: ToolRunner,
    provider_complete: Callable[..., Awaitable[Any]],
    prompt: str,
    system: str,
) -> str:
    """Call LLM; on tool JSON, run tool and call LLM again with results."""
    tool_notes: list[str] = []
    last_text = ""

    for _ in range(MAX_AGENT_STEPS):
        full_prompt = prompt
        if tool_notes:
            full_prompt += "\n\n--- Tool results (use to answer the user) ---\n"
            full_prompt += "\n\n".join(tool_notes)
            full_prompt += (
                "\n\nIf you have enough information, answer the user in plain language. "
                "Only emit another tool JSON if you still need more data."
            )

        response = await provider_complete(full_prompt, system)
        last_text = (getattr(response, "text", None) or str(response)).strip()
        call = parse_tool_call(last_text)
        if call is None:
            return last_text

        tool_name, args = call
        result = await tool_runner(tool_name, **args)
        tool_notes.append(format_tool_result(tool_name, result))

    if tool_notes:
        return last_text + "\n\n(Reached max tool steps; partial info above.)"
    return last_text
