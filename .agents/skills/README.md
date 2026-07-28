# Pocket Agent — Agent Skills Index

OKF module guides and Cursor skill packs for Pocket Agent development.

## OKF layers

| Layer | Path |
|-------|------|
| Feature contracts | [index.md](../../index.md) (repo root) |
| Feature specs | [specs/features/](../../specs/features/) |
| OKF skills index | [index.md](index.md) |
| Local modules | [modules/](modules/) |

## Local modules (OKF)

| Module | Use when |
|--------|----------|
| [architecture](modules/architecture.md) | Layer boundaries, source layout |
| [agent-protocol](modules/agent-protocol.md) | Reasoning, memory, approval gates |
| [tool-development](modules/tool-development.md) | `agent/tools/` implementation |
| [skill-authoring](modules/skill-authoring.md) | `agent/skills/` runtime modules |
| [file-safety](modules/file-safety.md) | Backup, validation, logging |
| [llm-routing](modules/llm-routing.md) | Provider abstraction |
| [telegram-interface](modules/telegram-interface.md) | Telegram bot layer |

## Cursor SKILL.md packs

| Pack | Use when |
|------|----------|
| [pocket-agent](pocket-agent/SKILL.md) | Starting any Pocket Agent task |
| [safe-file-ops](safe-file-ops/SKILL.md) | Safe file modification workflows |
| [add-tool](add-tool/SKILL.md) | Adding deterministic tools |
| [add-runtime-skill](add-runtime-skill/SKILL.md) | Adding domain skills |

## Extension order

1. Read **INSTRUCTIONS.md**, **ARCHITECTURE.md**, and root **index.md**
2. Check **ROADMAP.md** phase and matching **specs/features/** contract
3. Use **pocket-agent/SKILL.md** for implementation discipline
4. Add tools/skills per **add-tool** and **add-runtime-skill** packs
5. Update **TOOLS_SPEC.md**, **SKILLS.md**, and specs when behavior ships

## Runtime vs developer skills

| Path | Loaded by |
|------|-----------|
| `agent/skills/*.md` | Pocket Agent at runtime |
| `.agents/skills/` | Developers and Cursor |
