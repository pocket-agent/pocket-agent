"""Web search for current information (no API key required)."""

from __future__ import annotations

import asyncio
import logging

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)


def _normalize_item(item: dict) -> dict[str, str]:
    return {
        "title": str(item.get("title") or ""),
        "url": str(item.get("href") or item.get("link") or item.get("url") or ""),
        "snippet": str(item.get("body") or item.get("snippet") or item.get("description") or ""),
    }


def _search_sync(query: str, max_results: int) -> list[dict[str, str]]:
    """Try ddgs package (new) then duckduckgo_search (legacy)."""
    rows: list[dict[str, str]] = []

    try:
        from ddgs import DDGS

        ddgs = DDGS()
        backends = ("duckduckgo", "bing", "brave")
        for backend in backends:
            try:
                batch: list[dict[str, str]] = []
                for item in ddgs.text(query, max_results=max_results, backend=backend):
                    batch.append(_normalize_item(dict(item)))
                if batch:
                    logger.info("web_search: %d hits via ddgs backend=%s", len(batch), backend)
                    return batch
            except TypeError:
                # Older ddgs without backend= kwarg
                for item in ddgs.text(query, max_results=max_results):
                    batch.append(_normalize_item(dict(item)))
                if batch:
                    return batch
            except Exception as exc:
                logger.warning("web_search ddgs backend %s failed: %s", backend, exc)
        return rows
    except ImportError:
        pass

    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                rows.append(_normalize_item(dict(item)))
        if rows:
            logger.info("web_search: %d hits via duckduckgo_search", len(rows))
        return rows
    except ImportError:
        return []
    except Exception as exc:
        logger.warning("web_search duckduckgo_search failed: %s", exc)
        return []


async def web_search(query: str, max_results: int = 5) -> ToolResult:
    query = (query or "").strip()
    if not query:
        return ToolResult(success=False, error="query is required")

    max_results = max(1, min(int(max_results), 10))

    try:
        results = await asyncio.to_thread(_search_sync, query, max_results)
    except Exception as exc:
        logger.exception("web_search failed")
        return ToolResult(success=False, error=str(exc))

    if not results:
        logger.warning("web_search: zero results for query=%r", query)
        return ToolResult(
            success=True,
            data={
                "query": query,
                "results": [],
                "count": 0,
                "hint": "No web snippets returned. For weather use current_weather tool.",
            },
        )

    return ToolResult(
        success=True,
        data={
            "query": query,
            "results": results,
            "count": len(results),
        },
    )
