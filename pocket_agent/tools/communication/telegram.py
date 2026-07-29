from pocket_agent.logging.action_log import log_action
from pocket_agent.tools.base import ToolResult


async def send_telegram(
    bot,
    chat_id: int,
    text: str,
    logs_dir,
) -> ToolResult:
    """Send a Telegram message. See TOOLS_SPEC send_telegram()."""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        log_action(
            logs_dir,
            "send_telegram",
            {"chat_id": chat_id, "text_length": len(text)},
        )
        return ToolResult(success=True, data={"chat_id": chat_id})
    except Exception as exc:
        log_action(
            logs_dir,
            "send_telegram",
            {"chat_id": chat_id},
            success=False,
            error=str(exc),
        )
        return ToolResult(success=False, error=str(exc))
