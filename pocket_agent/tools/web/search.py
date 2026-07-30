"""Web search for current information (no API key required)."""

from __future__ import annotations

import asyncio
import logging

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)


async def web_search(query: str, max_results: int = 5) -> ToolResult:
    query = (query or "").strip()
    if not query:
        return ToolResult(success=False, error="query is required")

    max_results = max(1, min(int(max_results), 10))

    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return ToolResult(
            success=False,
            error="duckduckgo-search is not installed (pip install duckduckgo-search)",
        )

    def _run() -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                rows.append(
                    {
                        "title": str(item.get("title") or ""),
                        "url": str(item.get("href") or item.get("link") or ""),
                        "snippet": str(item.get("body") or item.get("snippet") or ""),
                    }
                )
        return rows

    try:
        results = await asyncio.to_thread(_run)
    except Exception as exc:
        logger.exception("web_search failed")
        return ToolResult(success=False, error=str(exc))

    return ToolResult(
        success=True,
        data={
            "query": query,
            "results": results,
            "count": len(results),
        },
    )
