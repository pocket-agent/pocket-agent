---
name: pocket-agent
description: >-
  Develop Pocket Agent — private self-hosted AI assistant. Use when implementing
  features, tools, skills, Telegram bot, LLM routing, NAS file access, or any
  Pocket Agent architecture work. Enforces tool-based execution and file safety.
---

# Pocket Agent development

You are developing Pocket Agent: a private personal AI assistant on user-owned infrastructure.

## Before coding

1. Read [INSTRUCTIONS.md](../../INSTRUCTIONS.md) and [ARCHITECTURE.md](../../ARCHITECTURE.md)
2. Check [ROADMAP.md](../../ROADMAP.md) for phase priority
3. Review matching spec in [specs/features/](../../specs/features/)
4. Plan minimally; add tests and docs

## Architecture rules

- **LLM reasons; tools execute** — never let the LLM directly modify files
- **Six layers:** Interface → Agent Core → Tools → Storage → Models
- **File pipeline:** Original → Backup → Working copy → Modify → Validate → Replace
- **Secrets:** `.env` only; never commit keys
- **LLM providers:** abstraction over Gemini, Claude, OpenAI, Ollama

## Source layout

```
agent/skills/   Runtime knowledge (markdown)
agent/tools/    Deterministic executors
agent/memory/   Persistent memory
agent/prompts/  System prompts
config/         llm.yaml, paths.yaml, settings.yaml
data/           logs/, working/, cache/, queue/
tests/
```

## Module guides

- [architecture](../modules/architecture.md)
- [agent-protocol](../modules/agent-protocol.md)
- [tool-development](../modules/tool-development.md)
- [skill-authoring](../modules/skill-authoring.md)
- [file-safety](../modules/file-safety.md)
- [llm-routing](../modules/llm-routing.md)
- [telegram-interface](../modules/telegram-interface.md)

## Reject implementations that

- Edit originals without backup
- Hardcode one LLM provider
- Delete or share externally without user approval
- Skip logging on file or tool operations
