"""Parse and run tool calls from LLM text responses."""

from __future__ import annotations

import json
import re
from collections.abc import Awaitable, Callable
from typing import Any

from pocket_agent.tools.base import ToolResult
from pocket_agent.tools.catalog import AGENT_TOOL_SPECS
from pocket_agent.tools.registry import ToolRegistry

MAX_AGENT_STEPS = 6

_FENCED_JSON_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


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
    data = result.data
    if tool_name == "web_search":
        lines = [f"[web_search] query={data.get('query')}"]
        for i, row in enumerate(data.get("results") or [], 1):
            lines.append(
                f"{i}. {row.get('title', '')}\n   {row.get('url', '')}\n   {row.get('snippet', '')}"
            )
        if len(lines) == 1:
            lines.append("No results.")
        return "\n".join(lines)
    return f"[{tool_name}] {json.dumps(data, ensure_ascii=False)[:4000]}"


async def run_agent_tool_loop(
    registry: ToolRegistry,
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
        result = await registry.run(tool_name, **args)
        tool_notes.append(format_tool_result(tool_name, result))

    if tool_notes:
        return last_text + "\n\n(Reached max tool steps; partial info above.)"
    return last_text
