---
type: Feature
title: Extension guidelines
description: How to add HTTP routes, tools, and CLI commands safely.
tags: [extension, guidelines]
timestamp: 2026-08-20T00:00:00Z
---

# Extension guidelines

1. Read [index.md](../../index.md) and [FEATURES.md](../FEATURES.md) before changing behavior.
2. New HTTP routes → update `pocket_agent/interface/`, mirror contracts in **pocket-agent-sdk**.
3. New tools → document in `TOOLS_SPEC.md`; follow AGENT_PROTOCOL safety rules.
4. Workspace paths → use `pocket_agent.workspace.paths`, not hardcoded sibling folder names.
5. Run `pytest` and `ruff check` before opening a PR.

Do not add React UI or Cloudflare Worker code to this repo.
