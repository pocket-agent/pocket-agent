# Architecture module

Recreate Pocket Agent's six-layer design when adding components.

## Layers

1. **Interface** — Telegram (now); dashboard/mobile later. Receives requests, authenticates, returns responses.
2. **Agent core** — Router, planner, memory manager, skill loader. Understands requests and selects actions.
3. **Tool layer** — Deterministic Python functions (`agent/tools/`). Never called by LLM as raw file I/O.
4. **Storage** — Synology NAS (documents), SQLite (runtime), optional vector DB.
5. **Model layer** — Replaceable providers: Gemini, Claude, OpenAI, Ollama.

## Boundaries

```
Interface → Agent Core → Skill → Tool → Storage/External API
```

The LLM lives inside agent core reasoning. It selects tools; it does not open files.

## Source paths

```
agent/skills/     Runtime knowledge (markdown)
agent/tools/      Executable capabilities
agent/memory/     Persistent memory
agent/prompts/    System prompts
config/           llm.yaml, paths.yaml, settings.yaml
data/logs/        Action logs
data/working/     Safe edit workspace
```

## References

- [ARCHITECTURE.md](../../../ARCHITECTURE.md)
- [specs/features/02-architecture.md](../../../specs/features/02-architecture.md)
