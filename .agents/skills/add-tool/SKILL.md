---
name: add-tool
description: >-
  Add a new Pocket Agent tool under agent/tools/. Use when implementing
  search_files, read_file, modify_excel, PDF tools, send_telegram, or any new
  deterministic agent capability.
---

# Add a Pocket Agent tool

Tools are deterministic functions. The LLM selects them; the runtime executes them.

## Checklist

1. **Implement** in `agent/tools/<category>/` with type hints (Python 3.12+)
2. **Validate** all inputs before execution
3. **Log** timestamp, tool name, inputs summary, result/errors
4. **Handle errors** — no silent failures
5. **File edits** — use [safe-file-ops](../safe-file-ops/SKILL.md) pipeline
6. **Document** in [TOOLS_SPEC.md](../../TOOLS_SPEC.md)
7. **Test** in `tests/tools/`
8. **Wire** into relevant `agent/skills/*.md` modules

## Tool template (conceptual)

```python
async def my_tool(param: str, path: str) -> ToolResult:
    """One-line purpose. See TOOLS_SPEC.md."""
    # validate inputs
    # execute deterministically
    # log action
    # return structured result
```

## Rules

- Tools do not call LLMs unless the tool's sole job is inference (e.g. summarize)
- Tools do not guess paths — use search or configured roots
- Every tool must have documentation in TOOLS_SPEC.md

## References

- [TOOLS_SPEC.md](../../TOOLS_SPEC.md)
- [modules/tool-development.md](../modules/tool-development.md)
- [specs/features/04-tool-system.md](../../specs/features/04-tool-system.md)
