# Pocket Agent — Development

Setup, dependencies, testing, and deployment for local development.

## Requirements

- Python 3.12+
- Telegram bot token ([BotFather](https://t.me/BotFather))
- Gemini API key (or local Ollama for optional routing)
- NAS mount path (Synology or local folder for dev)

## Quick start

```bash
# Clone and enter repo
cd pocket-agent

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install package + dev tools
pip install -e ".[dev]"

# Configure secrets
cp .env.example .env
# Edit .env: TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USER_IDS, GEMINI_API_KEY

# Optional: set NAS path in .env or config/paths.yaml
# NAS_ROOT=/Volumes/NAS/Documents

# Run the Telegram bot
pocket-agent
```

## Project layout

```
src/pocket_agent/     Python application
agent/skills/         Runtime skill modules (markdown)
agent/prompts/        System prompts
agent/memory/         Persistent memory (runtime)
config/               YAML configuration
data/                 logs, working, backup, cache, queue
tests/                pytest suite
```

## Configuration

| File | Purpose |
|------|---------|
| `.env` | Secrets and overrides (never commit) |
| `config/settings.yaml` | App settings |
| `config/paths.yaml` | NAS and data directories |
| `config/llm.yaml` | LLM providers and routing |

## Telegram commands

| Command | Action |
|---------|--------|
| `/start` | Welcome message |
| `/help` | Command list |
| `/nas` | List files on NAS root |
| `/search <query>` | Search file names on NAS |
| Any text | LLM response (Gemini when configured) |

## Testing

```bash
pytest
ruff check src tests
```

## Architecture reference

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [INSTRUCTIONS.md](INSTRUCTIONS.md)
- [specs/features/](specs/features/)

## Phase 1 status

Foundation scaffold: Python package, config loader, Gemini integration, Telegram bot, NAS list/search tools, action logging.

Next (Phase 2): file indexing, PDF extraction, document parsing.
