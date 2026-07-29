# Agent instructions — pocket-agent

**Scope:** this git repository (`pocket-agent/` locally, `pocket-agent` on GitHub).

Global workspace rules: [../INSTRUCTIONS.md](../INSTRUCTIONS.md) (read when developing inside the org folder).

## Contains

- `pocket_agent/` — Python package (`pip install -e`)
- `agent/` — runtime prompts, skills, memory
- `config/` — agent YAML (`llm.yaml`, `settings.yaml`)
- CLI entry: `pocket-agent` (serve, init, wizard, bootstrap)

## Shared contracts

Install `pocket_agent_sdk` from `../pocket-agent-sdk/python`. Use `CONNECTION_PROFILES` and `SERVICE_IDS` — do not hardcode profile or service strings.

## Do not duplicate here

- React UI → `../pocket-agent-web-app/`
- Worker → `../pocket-agent-api-app/`
- Shared types/schemas → `../pocket-agent-sdk/`
- Global OKF specs → `../specs/`
- Module registry → `../config/modules.yaml`

## Standalone clone

If only this repo is cloned, install `pocket-agent-sdk` from npm/PyPI when published, or clone the SDK sibling for workspace development.
