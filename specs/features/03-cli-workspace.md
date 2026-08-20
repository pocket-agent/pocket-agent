---
type: Feature
title: CLI and workspace
description: Module install, setup wizard server, and env bootstrap across sibling repos.
tags: [cli, workspace, yaml]
timestamp: 2026-08-20T00:00:00Z
---

# CLI and workspace

| Command | Purpose |
|---------|---------|
| `pocket-agent serve` | Start Pocket Node HTTP server |
| `pocket-agent init` | Install modules from `config/modules.yaml` |
| `pocket-agent setup` | Write `config/user-setup.yaml` |
| `pocket-agent wizard` | Serve setup UI + module install API |
| `pocket-agent bootstrap` | Sync `.env` / `pocket-agent-app` env files |

Workspace root is detected via `config/modules.yaml` or `config/setup.defaults.yaml` + nested `pocket-agent/`.

Module **`app`** maps to `pocket-agent-app` (replaces former separate web + api repos).
