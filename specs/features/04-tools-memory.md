---
type: Feature
title: Tools and memory
description: Agent skills, LLM routing, Telegram, and persistent memory policies.
tags: [tools, llm, memory, telegram]
timestamp: 2026-08-20T00:00:00Z
---

# Tools and memory

- Tool definitions: [TOOLS_SPEC.md](../../TOOLS_SPEC.md)
- Behavior rules: [AGENT_PROTOCOL.md](../../AGENT_PROTOCOL.md)
- LLM providers: `config/llm.yaml`
- Local dev: `AUTH_MODE=none` skips Google OAuth across the stack

Skills cover files, memory, weather, web fetch, calendar, reminders, and utilities. Never expose secrets or delete files silently.
