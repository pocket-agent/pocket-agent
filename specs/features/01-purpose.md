---
type: Feature
title: Purpose
description: Python Pocket Node — local AI agent with HTTP API, tools, and workspace integration.
tags: [python, agent, pocket-node, fastapi]
timestamp: 2026-08-20T00:00:00Z
---

# Purpose

**pocket-agent** is the Pocket Node: a Python package that runs on the user's machine, routes LLM requests, executes tools/skills, and exposes an HTTP API on `:8787`.

| Deliverable | Role |
|-------------|------|
| `pocket_agent/` | Python package (`pip install -e`) |
| `agent/` | Runtime prompts, skills, memory data |
| `config/` | Agent YAML (`llm.yaml`, `settings.yaml`) |
| CLI | `serve`, `telegram`, `init`, `setup`, `wizard`, `bootstrap` |

Sibling repos provide UI (`pocket-agent-app`), contracts (`pocket-agent-sdk`), and setup UX (`pocket-agent-wizard`). Do not duplicate those concerns here.
