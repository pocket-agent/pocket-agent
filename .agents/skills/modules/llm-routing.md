# LLM routing module

Recreate model abstraction when adding or changing LLM providers.

## Providers

Support all through one abstraction — never hardcode a single vendor:

- **Cloud:** Gemini, Claude, OpenAI
- **Local:** Ollama

## Routing examples

| Task | Preferred model |
|------|-----------------|
| Simple classification | Local (Ollama) |
| Complex reasoning | Gemini |
| Coding / tool planning | Claude |

## Configuration

Use `config/llm.yaml` for provider endpoints, model names, and routing rules. Secrets in `.env` only.

## Interface shape (conceptual)

```python
async def complete(prompt: str, task_type: str) -> str: ...
async def route(task_type: str) -> ModelProvider: ...
```

Agent core calls the abstraction; tools do not call LLMs directly unless the tool's sole purpose is LLM inference (e.g. summarization helper).

## References

- [INSTRUCTIONS.md](../../../INSTRUCTIONS.md) — LLM Rules
- [ARCHITECTURE.md](../../../ARCHITECTURE.md) — Model Layer
- [specs/features/07-development.md](../../../specs/features/07-development.md)
