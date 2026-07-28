---
type: Feature
title: Development
description: Coding standards, LLM abstraction, libraries, and implementation priority.
tags: [development]
timestamp: 2026-07-28T00:00:00Z
---

Guide for developers and coding agents. Canonical reference: [INSTRUCTIONS.md](../../INSTRUCTIONS.md).

## Stack

- Python 3.12+
- Type hints, async where useful
- Small modules, clear naming
- No giant files, hidden behavior, or hardcoded secrets

## File safety (mandatory)

```
Original → Backup → Working Copy → Modification → Validation → Replace
```

Never modify original files immediately. Every operation must create logs.

## LLM providers

Never hardcode one provider. Support Gemini, Claude, OpenAI, and Ollama through an abstraction layer.

## Task routing (example)

| Task type | Model |
|-----------|-------|
| Simple classification | Local (Ollama) |
| Complex reasoning | Gemini |
| Coding task | Claude |

## Implementation priority

1. Telegram communication
2. File indexing
3. NAS integration
4. Document reading
5. Safe editing
6. Memory
7. Dashboard

## Agent workflow before coding

1. Read all documentation
2. Understand architecture
3. Create a plan
4. Implement minimally
5. Add tests
6. Update documentation

Never implement features that violate architecture (especially direct LLM file modification).
