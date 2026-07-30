"""Tool metadata for the agentic loop (LLM tool selection)."""

from __future__ import annotations

from typing import Any

# Chat agent tools — no NAS/file or email integrations.
AGENT_TOOL_SPECS: dict[str, dict[str, Any]] = {
    "current_weather": {
        "description": (
            "Current weather and local time for a city (use for weather/temperature questions)."
        ),
        "parameters": {"location": "string — city name e.g. Amsterdam"},
    },
    "timezone_now": {
        "description": "Current local date and time for a city or place.",
        "parameters": {"location": "string — city name"},
    },
    "web_search": {
        "description": (
            "Search the public web for news, facts, prices, events. "
            "Do not use for Pocket Agent identity or GitHub — use system identity facts. "
            "For weather use current_weather; for page content use fetch_url."
        ),
        "parameters": {
            "query": "string — search query",
            "max_results": "optional int (1-10, default 5)",
        },
    },
    "fetch_url": {
        "description": "Download a web page and return readable text (use after web_search).",
        "parameters": {
            "url": "string — http(s) URL",
            "max_chars": "optional int (default 12000)",
        },
    },
    "exchange_rate": {
        "description": "Convert money using live ECB rates (Frankfurter API).",
        "parameters": {
            "from_currency": "3-letter code e.g. USD",
            "to_currency": "3-letter code e.g. EUR",
            "amount": "optional number (default 1)",
        },
    },
    "unit_convert": {
        "description": "Convert length, mass, or temperature units.",
        "parameters": {
            "value": "number",
            "from_unit": "string e.g. miles, kg, fahrenheit",
            "to_unit": "string e.g. km, pounds, celsius",
        },
    },
    "remember_memory": {
        "description": "Store a personal fact or preference for later recall.",
        "parameters": {
            "content": "string — what to remember",
            "category": "optional string e.g. preference, fact (default preference)",
        },
    },
    "recall_memory": {
        "description": "Recall stored personal memories matching a query.",
        "parameters": {"query": "string", "limit": "optional int"},
    },
    "search_knowledge": {
        "description": "Search the local knowledge base (indexed notes, not live web).",
        "parameters": {"query": "string", "limit": "optional int"},
    },
    "calendar_events": {
        "description": (
            "Upcoming calendar events from configured private ICS feed (read-only)."
        ),
        "parameters": {"days_ahead": "optional int 1-30 (default 7)"},
    },
    "schedule_reminder": {
        "description": "Schedule a reminder message at a future ISO datetime.",
        "parameters": {
            "message": "string",
            "when": "ISO-8601 datetime in the future e.g. 2026-07-30T18:00:00+02:00",
        },
    },
    "list_scheduled_tasks": {
        "description": "List pending scheduled reminders.",
        "parameters": {},
    },
    "cancel_task": {
        "description": "Cancel a pending reminder by task id.",
        "parameters": {"task_id": "string — reminder id (or first 8 chars)"},
    },
    "run_allowed_script": {
        "description": (
            "Run a maintenance script allowlisted in config (automation.allowed_scripts)."
        ),
        "parameters": {
            "script_name": "string — name from config",
            "timeout_seconds": "optional int",
        },
    },
}


def format_tool_catalog() -> str:
    lines = ["Available tools (invoke with JSON, see system rules):"]
    for name, spec in AGENT_TOOL_SPECS.items():
        params = ", ".join(f"{k}: {v}" for k, v in spec["parameters"].items())
        lines.append(f"- {name}: {spec['description']} Parameters: {params}")
    return "\n".join(lines)
