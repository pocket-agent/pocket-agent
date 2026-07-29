from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class LlmResponse:
    text: str
    provider: str
    model: str
    raw: Any | None = None


class LlmProvider(ABC):
    name: str

    @abstractmethod
    async def complete(self, prompt: str, system: str | None = None) -> LlmResponse:
        """Generate a completion for the given prompt."""
