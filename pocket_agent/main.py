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
    from pocket_agent.automation.reminders import ReminderStore
    from pocket_agent.automation.scheduler import ReminderScheduler, telegram_notify
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

    store = ReminderStore(runtime.settings.paths.queue_dir / "reminders.json")
    token = runtime.settings.env.telegram_bot_token

    async def _notify(reminder: dict) -> None:
        await telegram_notify(token, reminder)

    scheduler = ReminderScheduler(store, _notify)
    await scheduler.start()

    bot = TelegramBot(runtime.settings.env, runtime.agent)
    try:
        await bot.run_polling()
    finally:
        await scheduler.stop()


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


def run_agent_command(command: str) -> None:
    runtime = build_runtime()
    configure_logging(runtime.settings.env.log_level)
    logger = logging.getLogger("pocket_agent")

    if command == "telegram":
        asyncio.run(run_telegram(runtime))
    elif command == "serve":
        asyncio.run(run_serve(runtime))
    elif command == "run":
        if runtime.settings.env.telegram_bot_token:
            asyncio.run(run_both(runtime))
        else:
            logger.warning("TELEGRAM_BOT_TOKEN not set — starting HTTP only")
            asyncio.run(run_serve(runtime))


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        from pocket_agent.cli.init_modules import main as init_main

        sys.exit(init_main(sys.argv[2:]))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        from pocket_agent.cli.setup_wizard import main as setup_main

        sys.exit(setup_main(sys.argv[2:]))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "bootstrap":
        from pocket_agent.cli.bootstrap_cmd import main as bootstrap_main

        sys.exit(bootstrap_main(sys.argv[2:]))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "wizard":
        from pocket_agent.cli.workspace_wizard import main as wizard_main

        sys.exit(wizard_main(sys.argv[2:]))
        return

    parser = argparse.ArgumentParser(prog="pocket-agent")
    parser.add_argument(
        "command",
        nargs="?",
        default="telegram",
        choices=["telegram", "serve", "run", "init", "setup", "wizard", "bootstrap"],
        help="telegram|serve|run|init|setup|wizard|bootstrap",
    )
    args = parser.parse_args()

    if args.command == "init":
        from pocket_agent.cli.init_modules import run_init

        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
        sys.exit(run_init())
        return

    if args.command == "setup":
        from pocket_agent.cli.setup_wizard import run_setup

        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
        sys.exit(run_setup())
        return

    if args.command == "wizard":
        from pocket_agent.cli.workspace_wizard import run_wizard_server

        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
        sys.exit(run_wizard_server())
        return

    if args.command == "bootstrap":
        from pocket_agent.cli.bootstrap_cmd import main as bootstrap_main

        sys.exit(bootstrap_main())
        return

    run_agent_command(args.command)


if __name__ == "__main__":
    main()
