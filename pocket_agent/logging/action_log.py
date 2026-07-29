import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def log_action(
    logs_dir: Path,
    action: str,
    details: dict[str, Any],
    success: bool = True,
    error: str | None = None,
) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "success": success,
        "details": details,
        "error": error,
    }
    line = json.dumps(entry, default=str)
    logger.info("action=%s success=%s", action, success)

    log_file = logs_dir / f"actions_{datetime.now(UTC).strftime('%Y%m%d')}.jsonl"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
