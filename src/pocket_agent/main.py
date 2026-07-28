import argparse
import asyncio
import logging
import sys

from pocket_agent.runtime.bootstrap import build_runtime
from pocket_agent.runtime.context import AgentRuntime


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


async def run_telegram(runtime: AgentRuntime) -> None:
    from pocket_agent.interface.telegram_bot import TelegramBot

    if not runtime.settings.env.telegram_bot_token:
        logging.getLogger("pocket_agent").error(
            "TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and configure."
        )
        sys.exit(1)

    allowed = runtime.settings.env.allowed_user_ids()
    if not allowed:
        logging.getLogger("pocket_agent").warning(
            "TELEGRAM_ALLOWED_USER_IDS is empty — all users will be denied."
        )

    bot = TelegramBot(runtime.settings.env, runtime.agent)
    await bot.run_polling()


async def run_serve(runtime: AgentRuntime) -> None:
    from pocket_agent.interface.http_server import run_http_server

    await run_http_server(runtime)


async def run_both(runtime: AgentRuntime) -> None:
    from pocket_agent.interface.http_server import run_http_server

    http_task = asyncio.create_task(run_http_server(runtime))
    try:
        await run_telegram(runtime)
    finally:
        http_task.cancel()
        try:
            await http_task
        except asyncio.CancelledError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(prog="pocket-agent")
    parser.add_argument(
        "command",
        nargs="?",
        default="telegram",
        choices=["telegram", "serve", "run"],
        help="telegram: bot only; serve: HTTP API + static UI; run: both",
    )
    args = parser.parse_args()

    runtime = build_runtime()
    configure_logging(runtime.settings.env.log_level)
    logger = logging.getLogger("pocket_agent")

    if args.command == "telegram":
        asyncio.run(run_telegram(runtime))
    elif args.command == "serve":
        asyncio.run(run_serve(runtime))
    elif args.command == "run":
        if runtime.settings.env.telegram_bot_token:
            asyncio.run(run_both(runtime))
        else:
            logger.warning("TELEGRAM_BOT_TOKEN not set — starting HTTP only")
            asyncio.run(run_serve(runtime))


if __name__ == "__main__":
    main()
