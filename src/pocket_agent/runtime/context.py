from dataclasses import dataclass
from pathlib import Path

from pocket_agent.config.models import SettingsBundle
from pocket_agent.core.agent import AgentCore
from pocket_agent.llm.router import LlmRouter
from pocket_agent.memory.service import MemoryService


@dataclass
class AgentRuntime:
    settings: SettingsBundle
    project_root: Path
    llm_router: LlmRouter
    memory: MemoryService
    agent: AgentCore
