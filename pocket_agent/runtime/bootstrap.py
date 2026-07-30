import logging
from pathlib import Path

from pocket_agent.config.loader import ensure_data_dirs, load_settings
from pocket_agent.core.agent import AgentCore
from pocket_agent.core.skill_loader import load_skills, load_system_prompt
from pocket_agent.llm.router import LlmRouter
from pocket_agent.memory.service import MemoryService
from pocket_agent.runtime.context import AgentRuntime
from pocket_agent.tools.setup import build_tool_registry

logger = logging.getLogger(__name__)


def find_project_root() -> Path:
    from pocket_agent.workspace.paths import find_agent_root

    return find_agent_root()


def build_runtime(project_root: Path | None = None) -> AgentRuntime:
    root = project_root or find_project_root()
    settings = load_settings(root)
    ensure_data_dirs(settings.paths)

    llm_router = LlmRouter(settings.llm, settings.env, cache_dir=settings.paths.cache_dir)
    memory = MemoryService(settings.paths, settings.env, llm=settings.llm)
    tools = build_tool_registry(
        settings.paths,
        memory=memory,
        env=settings.env,
        project_root=root,
        raw_settings=settings.raw_settings,
    )
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

    logger.info(
        "Runtime ready — LLM: %s, memory: %d, knowledge: %d",
        llm_router.available_providers,
        memory.personal.count(),
        memory.knowledge.count(),
    )

    return AgentRuntime(
        settings=settings,
        project_root=root,
        llm_router=llm_router,
        memory=memory,
        agent=agent,
    )
