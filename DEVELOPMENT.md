# Development — pocket-agent

Python Pocket Node repository. Workspace layout: [../docs/WORKSPACE_LAYOUT.md](../docs/WORKSPACE_LAYOUT.md).

## Prerequisites

- Python 3.12+
- Sibling modules (web, api) for full stack — installed via `pocket-agent init`

## This repo

```
pocket-agent/
├── pocket_agent/     # Python package
├── agent/            # runtime skills, prompts, memory data
├── config/           # llm.yaml, settings.yaml, paths.yaml
├── tests/
└── pyproject.toml
```

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ../pocket-agent-sdk/python   # shared contracts
pip install -e ".[dev]"
```

## Workspace commands

From `pocket-agent/` with venv active:

- `pocket-agent wizard` — uses `../config/`, `../pocket-agent-wizard/`
- `pocket-agent init` — installs `pocket-agent-web-app`, etc. as siblings

## Local stack

See `../scripts/dev-desktop.sh` or `../scripts/dev-stack.sh`.

| Service | Directory | Port |
|---------|-----------|------|
| Agent (here) | `.` | 8787 |
| API | `../pocket-agent-api-app` | 8788 |
| Web | `../pocket-agent-web-app` | 5173 |

## Tests

```bash
pytest
ruff check pocket_agent tests
```
