# Development

This is the **pocket-agent** Python repository (`github.com/pocket-agent/pocket-agent`). Workspace layout: [../docs/WORKSPACE_LAYOUT.md](../docs/WORKSPACE_LAYOUT.md).

## Prerequisites

- Python 3.12+
- Node.js 20+ / Bun (sibling module packages)
- Optional: Rust (desktop)

## Workspace layout

```
../                          # org workspace (not this git repo)
├── config/modules.yaml
├── wizard/
├── pocket-agent/             # this repo
├── pocket-agent-web/
├── pocket-agent-api/
└── …
```

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pocket-agent wizard    # from workspace root config
```

## Local stack

From workspace root: `../scripts/dev-stack.sh`

| Service | Directory | Port |
|---------|-----------|------|
| Agent (here) | `.` | 8787 |
| API | `../pocket-agent-api` | 8788 |
| Web | `../pocket-agent-web` | 5173 |

## Tests

```bash
pytest
ruff check src tests
```

## Docs

- [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md)
- [docs/GOOGLE_OAUTH.md](docs/GOOGLE_OAUTH.md)
- [ROADMAP.md](ROADMAP.md)
