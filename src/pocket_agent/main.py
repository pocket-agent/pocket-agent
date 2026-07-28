import asyncio
import logging
import sys
from pathlib import Path


def _find_project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "config").is_dir():
        return cwd
    # src layout: repo root is parent of src/
    candidate = Path(__file__).resolve().parents[2]
    if (candidate / "config").is_dir():
        return candidate
    return cwd


async def run() -> None:
    from pocket_agent.config.loader import ensure_data_dirs, load_settings
    from pocket_agent.core.agent import AgentCore
    from pocket_agent.core.skill_loader import load_skills, load_system_prompt
    from pocket_agent.interface.telegram_bot import TelegramBot
    from pocket_agent.llm.router import LlmRouter
    from pocket_agent.memory.service import MemoryService
    from pocket_agent.tools.setup import build_tool_registry

    project_root = _find_project_root()
    settings = load_settings(project_root)
    ensure_data_dirs(settings.paths)

    logging.basicConfig(
        level=settings.env.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger = logging.getLogger("pocket_agent")

    if not settings.env.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and configure.")
        sys.exit(1)

    allowed = settings.env.allowed_user_ids()
    if not allowed:
        logger.warning("TELEGRAM_ALLOWED_USER_IDS is empty — all users will be denied.")

    llm_router = LlmRouter(settings.llm, settings.env)
    logger.info("LLM providers available: %s", llm_router.available_providers)

    memory = MemoryService(settings.paths, settings.env)
    logger.info(
        "Memory: embeddings=%s, memories=%d, knowledge_chunks=%d",
        memory.embeddings_available,
        memory.personal.count(),
        memory.knowledge.count(),
    )

    tools = build_tool_registry(settings.paths, memory=memory)
    skills = load_skills(settings.paths.skills_dir)
    system_prompt = load_system_prompt(settings.paths.prompts_dir)

    agent = AgentCore(
        llm_router=llm_router,
        tools=tools,
        skills=skills,
        system_prompt=system_prompt,
        logs_dir=settings.paths.logs_dir,
        memory=memory,
    )

    bot = TelegramBot(settings.env, agent)
    await bot.run_polling()


def main() -> None:
    asyncio.run(run())
