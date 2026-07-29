from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine


@dataclass
class ToolResult:
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


ToolHandler = Callable[..., Coroutine[Any, Any, ToolResult]]
