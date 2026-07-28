# Pocket Agent Index


## Purpose

This document explains the repository structure and responsibilities.


# Documentation


## README.md

Project overview.

Contains:

- Vision
- Features
- Architecture summary


## INSTRUCTIONS.md

Main instructions for AI coding agents.

Used by:

- Cursor
- Developers
- Future contributors


Defines:

- Coding rules
- Architecture constraints
- Implementation principles


## ARCHITECTURE.md

Technical architecture.

Defines:

- Components
- Data flow
- Services
- Communication


## SECURITY.md

Security model.

Defines:

- Permissions
- Secrets
- File safety
- Backup strategy


## DEVELOPMENT.md

Developer workflow.

Contains:

- Setup
- Dependencies
- Testing
- Deployment


## ROADMAP.md

Feature development roadmap.


## SKILLS.md

Defines the skill system.


## TOOLS_SPEC.md

Defines available tools exposed to the agent.


## AGENT_PROTOCOL.md

Defines how the agent reasons and operates.


# Source Structure


## Monorepo (`apps/`)

| App | Path | Purpose |
|-----|------|---------|
| Web | [apps/web/](apps/web/) | React dashboard — Cloudflare Pages or local static serve |
| Desktop | [apps/desktop/](apps/desktop/) | Tauri shell — same UI, local-first on macOS/Windows/Linux |

See [apps/README.md](apps/README.md).


## Python agent (`src/pocket_agent/`)

Telegram interface, agent core, tools, memory, LLM routing. Entry point: `pocket-agent` CLI.


## Runtime agent (`agent/`)

Markdown skills, system prompts, persistent memory data — not Python packages.


Contains:

```
skills/
prompts/
memory/
```


## skills/

Knowledge modules (runtime). Examples: `pdf.md`, `excel.md`, `files.md`, `memory.md`.


## tools/

Python implementations live in `src/pocket_agent/tools/`. See [agent/tools/README.md](agent/tools/README.md).


## memory/

Persistent agent memory directory (runtime files).


## config/

Configuration files.


Examples:

```
llm.yaml

paths.yaml

settings.yaml

```


## data/

Runtime information.

Contains:

```
logs/

queue/

working/

cache/

```


# Development Rule

Every feature must include:

- Documentation
- Tests
- Error handling
- Security consideration


# OKF Specs

Numbered feature contracts derived from the docs above:

* [specs/features/index.md](specs/features/index.md)

| Spec | Topic |
|------|-------|
| [01 — Purpose](specs/features/01-purpose.md) | Vision and constraints |
| [02 — Architecture](specs/features/02-architecture.md) | Six layers and layout |
| [03 — Agent protocol](specs/features/03-agent-protocol.md) | Reasoning and approval |
| [04 — Tool system](specs/features/04-tool-system.md) | Deterministic tools |
| [05 — Skill system](specs/features/05-skill-system.md) | Runtime skills |
| [06 — Security](specs/features/06-security.md) | Secrets, backups, logging |
| [07 — Development](specs/features/07-development.md) | Stack and priorities |
| [08 — Roadmap](specs/features/08-roadmap.md) | Phased delivery |
| [09 — Extension guidelines](specs/features/09-extension-guidelines.md) | Adding tools and skills |


# Agent Skills (developers)

Cursor and coding-agent guides — not runtime `agent/skills/`:

* [.agents/skills/README.md](.agents/skills/README.md) — catalog
* [.agents/skills/index.md](.agents/skills/index.md) — OKF skills index
* [modules/](.agents/skills/modules/) — recreation guides
* Cursor packs: `pocket-agent`, `safe-file-ops`, `add-tool`, `add-runtime-skill`