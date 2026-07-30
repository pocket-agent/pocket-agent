"""Read-only calendar events from a private ICS feed URL."""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
import httpx
from icalendar import Calendar

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)


def _parse_ics_events(raw: bytes, days_ahead: int) -> list[dict[str, str]]:
    cal = Calendar.from_ical(raw)
    now = datetime.now(UTC)
    horizon = now + timedelta(days=days_ahead)
    events: list[tuple[datetime, dict[str, str]]] = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        dtstart = component.get("dtstart")
        if dtstart is None:
            continue
        start = dtstart.dt
        if isinstance(start, datetime):
            if start.tzinfo is None:
                start = start.replace(tzinfo=UTC)
            start_utc = start.astimezone(UTC)
        else:
            start_utc = datetime(start.year, start.month, start.day, tzinfo=UTC)

        if start_utc < now - timedelta(hours=12) or start_utc > horizon:
            continue

        title = str(component.get("summary", "Event"))
        location = str(component.get("location", ""))
        desc = str(component.get("description", ""))[:200]
        events.append(
            (
                start_utc,
                {
                    "title": title,
                    "start": start_utc.isoformat(),
                    "location": location,
                    "description": desc,
                },
            )
        )

    events.sort(key=lambda item: item[0])
    return [row for _, row in events[:50]]


async def calendar_events(ics_url: str, days_ahead: int = 7) -> ToolResult:
    url = (ics_url or "").strip()
    if not url:
        return ToolResult(
            success=False,
            error="Calendar ICS URL is not configured (set CALENDAR_ICS_URL in .env)",
        )

    days_ahead = max(1, min(int(days_ahead), 30))

    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            events = _parse_ics_events(response.content, days_ahead)

        if not events:
            return ToolResult(
                success=True,
                data={
                    "days_ahead": days_ahead,
                    "count": 0,
                    "events": [],
                    "summary": f"No events in the next {days_ahead} days.",
                },
            )

        lines = [f"Upcoming events ({len(events)}):"]
        for ev in events[:15]:
            lines.append(f"- {ev['start']}: {ev['title']}")
        return ToolResult(
            success=True,
            data={
                "days_ahead": days_ahead,
                "count": len(events),
                "events": events,
                "summary": "\n".join(lines),
            },
        )
    except httpx.HTTPError as exc:
        logger.exception("calendar_events HTTP error")
        return ToolResult(success=False, error=f"Could not fetch calendar: {exc}")
    except Exception as exc:
        logger.exception("calendar_events failed")
        return ToolResult(success=False, error=str(exc))
