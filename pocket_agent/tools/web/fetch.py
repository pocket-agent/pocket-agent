"""Fetch and extract readable text from a public URL."""

from __future__ import annotations

import logging
import re

import httpx

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)

_MAX_BYTES = 500_000
_MAX_CHARS = 12_000

_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_BLOCK_END_RE = re.compile(r"</(p|div|h[1-6]|li|tr)>", re.IGNORECASE)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t]+")
_BLANK_RE = re.compile(r"\n{3,}")


def _html_to_text(html: str) -> str:
    text = _TAG_RE.sub("", html)
    text = _BR_RE.sub("\n", text)
    text = _BLOCK_END_RE.sub("\n", text)
    text = _TAG_STRIP_RE.sub(" ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = _WS_RE.sub(" ", text)
    lines = [ln.strip() for ln in text.splitlines()]
    text = "\n".join(ln for ln in lines if ln)
    return _BLANK_RE.sub("\n\n", text).strip()


async def fetch_url(url: str, max_chars: int = _MAX_CHARS) -> ToolResult:
    target = (url or "").strip()
    if not target:
        return ToolResult(success=False, error="url is required")
    if not re.match(r"^https?://", target, re.IGNORECASE):
        return ToolResult(success=False, error="url must start with http:// or https://")

    max_chars = max(500, min(int(max_chars), _MAX_CHARS))

    try:
        async with httpx.AsyncClient(
            timeout=25.0,
            follow_redirects=True,
            headers={"User-Agent": "PocketAgent/1.0 (personal assistant)"},
        ) as client:
            response = await client.get(target)
            response.raise_for_status()
            raw = response.content[:_MAX_BYTES]
            content_type = (response.headers.get("content-type") or "").lower()

            if "html" in content_type or raw[:15].decode("utf-8", errors="ignore").lstrip().startswith("<"):
                text = _html_to_text(raw.decode("utf-8", errors="replace"))
                kind = "html"
            else:
                text = raw.decode("utf-8", errors="replace")
                kind = "text"

            truncated = len(text) > max_chars
            if truncated:
                text = text[:max_chars]

            return ToolResult(
                success=True,
                data={
                    "url": str(response.url),
                    "content_type": content_type or kind,
                    "text": text,
                    "truncated": truncated,
                    "length": len(text),
                },
            )
    except httpx.HTTPError as exc:
        logger.warning("fetch_url HTTP error for %s: %s", target, exc)
        return ToolResult(success=False, error=f"Could not fetch URL: {exc}")
    except Exception as exc:
        logger.exception("fetch_url failed")
        return ToolResult(success=False, error=str(exc))
