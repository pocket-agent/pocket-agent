# pocket-agent (Pocket Node)

Python agent — LLM routing, tools, memory, Telegram, and `pocket-agent serve`.

Part of the open-source **[Pocket Agent](https://github.com/pocket-agent)** ecosystem · **v0.1.0**

**GitHub:** [pocket-agent/pocket-agent](https://github.com/pocket-agent/pocket-agent)

## What's included (0.1.0)

- **Pocket Node HTTP API** — `/health`, `/status`, `/me`, `/chat` on `:8787`
- **CLI** — `serve`, `telegram`, `init`, `setup`, `wizard`, `bootstrap`
- **Tools & skills** — file pipeline, memory, configurable LLM routing
- **Workspace commands** — install sibling modules, run setup wizard, sync env files
- **Shared types** — `pocket_agent_sdk` from [pocket-agent-sdk](../pocket-agent-sdk/)

## Quick start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ../pocket-agent-sdk/python   # workspace
pip install -e ".[dev]"
pocket-agent serve
```

Full workspace: [../scripts/setup-local.sh](../scripts/setup-local.sh) · Wizard: `pocket-agent wizard`

## Docs

[DEVELOPMENT.md](DEVELOPMENT.md) · [INSTRUCTIONS.md](INSTRUCTIONS.md) · [CHANGELOG.md](CHANGELOG.md) · [AGENT_PROTOCOL.md](AGENT_PROTOCOL.md) · [TOOLS_SPEC.md](TOOLS_SPEC.md)

Global OKF (workspace): [../INSTRUCTIONS.md](../INSTRUCTIONS.md) · [../ROADMAP.md](../ROADMAP.md)
