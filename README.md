# pocket-agent (Python core)

Private, self-hosted personal AI assistant — **Pocket Node**.

Git repo: `github.com/pocket-agent/pocket-agent`. Workspace context: [../README.md](../README.md).

## Quick start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pocket-agent wizard    # workspace wizard — ../config/, ../wizard/
pocket-agent serve     # :8787
```

## Commands

| Command | Description |
|---------|-------------|
| `serve` | HTTP API (Pocket Node) |
| `telegram` | Telegram bot |
| `init` | Install sibling modules (latest GitHub releases) |
| `setup` | Write `../config/user-setup.yaml` |
| `wizard` | Liquid-glass setup UI |

## Docs in this repo

[AGENT_PROTOCOL.md](AGENT_PROTOCOL.md) · [TOOLS_SPEC.md](TOOLS_SPEC.md) · [DEVELOPMENT.md](DEVELOPMENT.md) · [INSTRUCTIONS.md](INSTRUCTIONS.md)

## Global workspace docs

[../INSTRUCTIONS.md](../INSTRUCTIONS.md) · [../specs/](../specs/) · [../.agents/skills/](../.agents/skills/)
