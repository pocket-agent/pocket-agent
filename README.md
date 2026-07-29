# pocket-agent (Pocket Node)

Python agent — LLM routing, tools, memory, Telegram, `pocket-agent serve`.

**GitHub:** [pocket-agent/pocket-agent](https://github.com/pocket-agent/pocket-agent)

When developed inside the org workspace, global docs live at the parent folder: [../README.md](../README.md), [../INSTRUCTIONS.md](../INSTRUCTIONS.md), [../ROADMAP.md](../ROADMAP.md).

## Quick start (standalone or workspace)

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pocket-agent serve     # :8787
```

In a full workspace clone, run `pocket-agent wizard` from here (uses `../pocket-agent-wizard/` and `../config/`).

## CLI commands

| Command | Description |
|---------|-------------|
| `serve` | Pocket Node HTTP API |
| `telegram` | Telegram bot |
| `init` | Install sibling modules from releases |
| `setup` | Write `../config/user-setup.yaml` |
| `wizard` | Workspace setup UI |
| `bootstrap` | Env file templates |

## Repo docs

[AGENT_PROTOCOL.md](AGENT_PROTOCOL.md) · [TOOLS_SPEC.md](TOOLS_SPEC.md) · [DEVELOPMENT.md](DEVELOPMENT.md) · [INSTRUCTIONS.md](INSTRUCTIONS.md)

Standalone clone: [ROADMAP.md](ROADMAP.md). In workspace, see [../ROADMAP.md](../ROADMAP.md).
