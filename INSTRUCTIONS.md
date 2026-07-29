# Agent instructions — core

**Scope:** this git repository (`pocket-agent/` locally, `pocket-agent` on GitHub).

Global workspace rules: [../INSTRUCTIONS.md](../INSTRUCTIONS.md) (read when developing inside the org folder).

## Contains

- `pocket_agent/` — Python package (`pip install -e`)
- `agent/` — runtime prompts, skills, memory
- `config/` — agent YAML (`llm.yaml`, `settings.yaml`)
- CLI entry: `pocket-agent` (serve, init, wizard, bootstrap)

## Do not duplicate here

- React UI → `../pocket-agent-web-app/`
- Worker → `../pocket-agent-api-app/`
- Global OKF specs → `../specs/`
- Module registry → `../config/modules.yaml`

## Standalone clone

If only this repo is cloned, you still have agent docs here but no workspace wizard until sibling folders exist.
