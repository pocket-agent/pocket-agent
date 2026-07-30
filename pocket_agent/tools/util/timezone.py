"""Local time for a city or place (Open-Meteo geocoding)."""

from __future__ import annotations

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)


async def timezone_now(location: str) -> ToolResult:
    place = (location or "").strip()
    if not place:
        return ToolResult(success=False, error="location is required")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            geo = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": place, "count": 1, "language": "en", "format": "json"},
            )
            geo.raise_for_status()
            results = geo.json().get("results") or []
            if not results:
                return ToolResult(success=False, error=f"No location found for '{place}'")

            hit = results[0]
            name = hit.get("name", place)
            country = hit.get("country", "")
            tz_name = hit.get("timezone", "UTC")
            now = datetime.now(ZoneInfo(tz_name))
            summary = f"{name}, {country}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')} ({tz_name})"

            return ToolResult(
                success=True,
                data={
                    "location": name,
                    "country": country,
                    "timezone": tz_name,
                    "local_time": now.isoformat(),
                    "summary": summary,
                },
            )
    except httpx.HTTPError as exc:
        logger.exception("timezone_now HTTP error")
        return ToolResult(success=False, error=str(exc))
    except Exception as exc:
        logger.exception("timezone_now failed")
        return ToolResult(success=False, error=str(exc))
