from pathlib import Path

import pytest

from pocket_agent.core.agent import AgentCore
from pocket_agent.core.skill_loader import load_skills, load_system_prompt
from pocket_agent.llm.router import LlmRouter
from pocket_agent.config.models import AppSettings, LlmConfig, PathsConfig
from pocket_agent.tools.setup import build_tool_registry


def _agent(tmp_path: Path) -> AgentCore:
    nas = tmp_path / "nas"
    nas.mkdir()
    (nas / "doc.txt").write_text("hello")

    paths = PathsConfig(
        {
            "nas": {"root": str(nas), "allowed_read_roots": [str(nas)]},
            "data": {"logs": "data/logs"},
        },
        tmp_path,
    )
    paths.logs_dir.mkdir(parents=True, exist_ok=True)

    env = AppSettings()
    llm = LlmConfig({"default_provider": "gemini", "providers": {}})
    router = LlmRouter(llm, env)
    tools = build_tool_registry(paths)
    skills = load_skills(Path(__file__).resolve().parents[1] / "agent" / "skills")
    system = load_system_prompt(Path(__file__).resolve().parents[1] / "agent" / "prompts")

    return AgentCore(
        llm_router=router,
        tools=tools,
        skills=skills,
        system_prompt=system,
        logs_dir=paths.logs_dir,
    )


@pytest.mark.asyncio
async def test_nas_command_without_llm(tmp_path: Path):
    agent = _agent(tmp_path)
    reply = await agent.handle_message("/nas")
    assert "doc.txt" in reply
