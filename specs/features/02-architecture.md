---
type: Feature
title: Architecture
description: Six-layer system design from interface through models and storage.
tags: [architecture]
timestamp: 2026-07-28T00:00:00Z
---

Pocket Agent consists of six layers. See [ARCHITECTURE.md](../../ARCHITECTURE.md) for the full reference.

## Layers

| Layer | Responsibility | Current / planned |
|-------|----------------|-------------------|
| Interface | User communication, auth | Telegram (now); web dashboard, mobile (future) |
| Agent core | Reasoning, planning, memory, skills | Router, planner, memory manager, skill loader |
| Tool layer | Deterministic execution | `search_files`, `read_file`, `modify_excel`, etc. |
| Storage | Documents and runtime state | Synology NAS (primary), SQLite (runtime), optional vector DB |
| Model layer | LLM providers | Gemini, Claude, OpenAI (cloud); Ollama (local) |

## Data flow (search example)

```
Telegram → Agent Core → Search Skill → NAS Search Tool → Document Found → Telegram Response
```

## Data flow (editing example)

```
User Request → Agent Planning → Backup → Working Copy → Tool Execution → Validation → Save → Notify User
```

## Source layout

```
src/
agent/
  skills/    # Runtime knowledge modules (markdown)
  tools/     # Executable capabilities
  memory/    # Persistent agent memory
  prompts/   # System and task prompts
config/      # llm.yaml, paths.yaml, settings.yaml
data/        # logs/, queue/, working/, cache/
tests/
```

## Implementation rule

Every layer boundary must be respected: interfaces talk to agent core; agent core selects skills and tools; tools touch files and external APIs — never the LLM directly.
