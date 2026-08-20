# Agent & developer instructions — pocket-agent

**pocket-agent** — Python **Pocket Node**: LLM routing, tools, memory, Telegram, and `pocket-agent serve` on `:8787`.

## What ships out of the box

| Surface | Area | Description |
|---------|------|-------------|
| `GET /health` | HTTP | Liveness probe |
| `GET /status` | HTTP | Agent status |
| `POST /chat` | HTTP | Chat via Pocket Node |
| `/me`, `/settings/*` | HTTP | Profile and settings |
| CLI | `pocket_agent.cli` | `serve`, `init`, `setup`, `wizard`, `bootstrap` |
| Tools | `agent/` skills | Files, memory, web, calendar, … |

Details: [`index.md`](index.md) · Feature specs: [`specs/`](specs/)

## Key modules

| Area | Path |
|------|------|
| HTTP app | `pocket_agent/interface/http_app.py` |
| CLI | `pocket_agent/cli/` |
| Workspace paths | `pocket_agent/workspace/paths.py` |
| Bootstrap | `pocket_agent/cli/workspace_bootstrap.py` |
| Agent config | `config/settings.yaml`, `config/llm.yaml` |

## Shared contracts

Install `pocket_agent_sdk` from `../pocket-agent-sdk/python`. Use `CONNECTION_PROFILES` and `SERVICE_IDS` — do not hardcode profile or service strings.

## Do not duplicate here

| Concern | Repo |
|---------|------|
| Fullstack UI + API | `../pocket-agent-app/` |
| Shared types/schemas | `../pocket-agent-sdk/` |
| Module registry | `../config/modules.yaml` (workspace) |

## Local development

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ../pocket-agent-sdk/python
pip install -e ".[dev]"
pocket-agent serve
pytest
```

Full workspace: `../scripts/setup-local.sh` or `pocket-agent wizard`.

## Agent checklist

1. Read [index.md](index.md) and [specs/FEATURES.md](specs/FEATURES.md).
2. Match existing patterns in `pocket_agent/` before adding routes or tools.
3. Update **pocket-agent-sdk** when HTTP or setup contracts change.
4. Never commit secrets (`.env`, API keys).

## Repository documents

[README](README.md) | **INSTRUCTIONS** | [DEVELOPMENT](DEVELOPMENT.md) | [CHANGELOG](CHANGELOG.md) | [CONTRIBUTING](CONTRIBUTING.md) | [SECURITY](SECURITY.md) | [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)
