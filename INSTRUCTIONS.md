# Agent instructions — pocket-agent (Python core)

**Scope:** this git repository only. Global workspace rules: [../INSTRUCTIONS.md](../INSTRUCTIONS.md).

## This repo contains

- `src/pocket_agent/` — Python package
- `agent/` — runtime prompts, skills, memory data
- `config/` — `llm.yaml`, `settings.yaml`, `paths.yaml`
- `tests/`
- CLI: `pocket-agent serve`, `telegram`, `init`, `setup`, `wizard`

## Key docs (this repo)

| File | Purpose |
|------|---------|
| [AGENT_PROTOCOL.md](AGENT_PROTOCOL.md) | How the agent reasons |
| [TOOLS_SPEC.md](TOOLS_SPEC.md) | Tool contracts |
| [SKILLS.md](SKILLS.md) | Runtime skill system |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Dev workflow |

## Cross-repo docs (workspace)

| Topic | Path |
|-------|------|
| OKF specs | [../specs/](../specs/) |
| Architecture | [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) |
| Apps flow | [../docs/APPS_ARCHITECTURE.md](../docs/APPS_ARCHITECTURE.md) |
| Developer skills | [../.agents/skills/](../.agents/skills/) |

## Do not add here

- React UI → `../pocket-agent-web/`
- Cloudflare Worker → `../pocket-agent-api/`
- Workspace module registry → `../config/modules.yaml`

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pocket-agent wizard   # uses ../config/ and ../wizard/
```
