"""Currency conversion via Frankfurter (ECB rates, no API key)."""

from __future__ import annotations

import logging
import re

import httpx

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)

_CURRENCY_RE = re.compile(r"^[A-Za-z]{3}$")


async def exchange_rate(
    from_currency: str,
    to_currency: str,
    amount: float = 1.0,
) -> ToolResult:
    src = (from_currency or "").strip().upper()
    dst = (to_currency or "").strip().upper()
    if not _CURRENCY_RE.match(src) or not _CURRENCY_RE.match(dst):
        return ToolResult(success=False, error="from_currency and to_currency must be 3-letter codes")

    try:
        amt = float(amount)
    except (TypeError, ValueError):
        return ToolResult(success=False, error="amount must be a number")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                "https://api.frankfurter.app/latest",
                params={"from": src, "to": dst, "amount": amt},
            )
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get(dst)
            if rate is None:
                return ToolResult(success=False, error=f"Rate not available for {src} → {dst}")

            converted = float(rate)
            summary = f"{amt} {src} = {converted:.4f} {dst} (rate date {data.get('date')})"
            return ToolResult(
                success=True,
                data={
                    "from": src,
                    "to": dst,
                    "amount": amt,
                    "converted": converted,
                    "rate_date": data.get("date"),
                    "summary": summary,
                },
            )
    except httpx.HTTPError as exc:
        logger.exception("exchange_rate HTTP error")
        return ToolResult(success=False, error=str(exc))
    except Exception as exc:
        logger.exception("exchange_rate failed")
        return ToolResult(success=False, error=str(exc))
