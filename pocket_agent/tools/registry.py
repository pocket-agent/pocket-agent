from pocket_agent.tools.base import ToolHandler, ToolResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._tools[name] = handler

    def get(self, name: str) -> ToolHandler | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools.keys())

    async def run(self, name: str, **kwargs: object) -> ToolResult:
        handler = self.get(name)
        if handler is None:
            return ToolResult(success=False, error=f"Unknown tool: {name}")
        return await handler(**kwargs)
