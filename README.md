# pocket-agent (Python core)

Private, self-hosted personal AI assistant — Pocket Node.

Part of the Pocket Agent **workspace** (sibling to `pocket-agent-web`, `pocket-agent-api`, etc.). See the [workspace README](../README.md).

## Quick start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pocket-agent wizard    # or: pocket-agent setup && pocket-agent init
pocket-agent serve     # :8787
```

## Commands

| Command | Description |
|---------|-------------|
| `pocket-agent serve` | HTTP API (Pocket Node) |
| `pocket-agent telegram` | Telegram bot |
| `pocket-agent init` | Install modules from latest GitHub releases |
| `pocket-agent setup` | Write workspace `config/user-setup.yaml` |
| `pocket-agent wizard` | Open liquid-glass setup UI |
