"""Tool metadata for the agentic loop (LLM tool selection)."""

from __future__ import annotations

from typing import Any

# Tools the chat agent may invoke via JSON (see agent/tool_loop.py).
AGENT_TOOL_SPECS: dict[str, dict[str, Any]] = {
    "current_weather": {
        "description": (
            "Current weather and local time for a city or place (use for weather/temperature "
            "questions — more reliable than web_search)."
        ),
        "parameters": {"location": "string — city name e.g. Amsterdam"},
    },
    "web_search": {
        "description": (
            "Search the public web for news, facts, prices, events. "
            "For weather or local time prefer current_weather."
        ),
        "parameters": {
            "query": "string — search query",
            "max_results": "optional int (1-10, default 5)",
        },
    },
    "search_files": {
        "description": "Search indexed NAS/local files by keyword (not the web).",
        "parameters": {
            "query": "string",
            "location": "optional folder under NAS",
            "extension": "optional file extension",
            "limit": "optional int",
        },
    },
    "read_file": {
        "description": "Read text from a file on NAS.",
        "parameters": {"file_path": "string path", "max_chars": "optional int"},
    },
    "recall_memory": {
        "description": "Recall stored personal memories matching a query.",
        "parameters": {"query": "string", "limit": "optional int"},
    },
    "search_knowledge": {
        "description": "Search the local knowledge base (indexed documents).",
        "parameters": {"query": "string", "limit": "optional int"},
    },
}


def format_tool_catalog() -> str:
    lines = ["Available tools (invoke with JSON, see system rules):"]
    for name, spec in AGENT_TOOL_SPECS.items():
        params = ", ".join(f"{k}: {v}" for k, v in spec["parameters"].items())
        lines.append(f"- {name}: {spec['description']} Parameters: {params}")
    return "\n".join(lines)
