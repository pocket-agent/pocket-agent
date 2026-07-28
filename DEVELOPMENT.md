# Pocket Agent — Development

Setup, monorepo layout, testing, and deployment.

## Requirements

- Python 3.12+ (agent core)
- Node.js 20+ / Bun (app packages in `apps/`)
- Google Cloud OAuth client (web + desktop — shared client ID)
- Telegram bot token, Gemini API key (see `.env.example`)
- NAS mount or local folder for development
- Cloudflare account (Pages + Worker deploy)
- Optional: `cloudflared` for exposing Pocket Node to hosted web

## Monorepo layout

```
pocket-agent/
├── apps/
│   ├── web/          # pocket-agent-web-app → Cloudflare Pages
│   ├── api/          # pocket-agent-api-app → Cloudflare Worker
│   ├── desktop/      # Tauri (desktop install)
│   └── cli/          # pocket-agent-cli (future, desktop install)
├── src/pocket_agent/ # Python agent (Pocket Node)
├── agent/            # Runtime skills & prompts
├── config/           # YAML config (includes apps.yaml)
├── docs/             # APPS_ARCHITECTURE.md
└── tests/
```

See [apps/README.md](apps/README.md) and [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md).

# First-time monorepo setup

```bash
cd pocket-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

pocket-agent setup   # all-local profile → config/user-setup.yaml
pocket-agent init    # clone web + api repos (+ runs setup if needed)
```

Default profile **`all-local`**: web (Vite), API (Hono `wrangler dev`), agent (`pocket-agent serve`). No Cloudflare deploy required.

API stack: **Hono** on Workers — see [docs/API_STACK.md](docs/API_STACK.md).

## Agent (Pocket Node)

```bash
pocket-agent           # Telegram bot (default)
pocket-agent serve     # HTTP API on :8787 (tools, LLM, memory)
pocket-agent run       # Telegram + HTTP together
```

The Python agent holds LLM API keys and executes tools. Hosted web does not call LLM providers directly — the API worker proxies to this service (local or via Cloudflare Tunnel).

## Local full stack (target)

```bash
# Terminal 1 — Pocket Node
pocket-agent serve

# Terminal 2 — API worker (after apps/api template lands)
cd apps/api && npm run dev

# Terminal 3 — Web
cd apps/web && bun install && bun run dev
```

## Deployment

| Component | Target |
|-----------|--------|
| `apps/web` | Cloudflare Pages |
| `apps/api` | Cloudflare Worker |
| Agent | Pocket Node + optional `cloudflared tunnel` |
| `apps/desktop`, `apps/cli` | Desktop install only |

Production flow: Pages web → Worker API → tunnel URL → `pocket-agent serve`.

## Telegram commands

| Command | Action |
|---------|--------|
| `/start` | Welcome message |
| `/help` | Command list |
| `/index` | Rebuild SQLite file index on NAS |
| `/nas` | List files at NAS root |
| `/search <query>` | Search indexed files (name/path) |
| `/read <path>` | Read TXT, DOCX, PDF, or XLSX summary |
| `/pdf <path>` | Extract PDF text |
| `/excel <path>` | Analyze Excel workbook structure |
| `/edit_excel <path> <sheet> <cell>=<value>` | Safe single-cell Excel edit |
| `/edit_word <path> append\|replace_last <text>` | Safe Word paragraph edit |
| `/edit_pdf <path> add_page <text>` | Add PDF page with text |
| `/remember <text>` | Store personal memory (no secrets) |
| `/recall <query>` | Search your memories |
| `/kb <query>` | Search knowledge base |
| `/kb_index` | Index NAS text/PDF into knowledge base |
| Any text | LLM with memory + skill context (Gemini when configured) |

## Testing

```bash
pytest
ruff check src tests
```

## Architecture reference

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md)
- [INSTRUCTIONS.md](INSTRUCTIONS.md)
- [specs/features/](specs/features/)
- [apps/README.md](apps/README.md)

## Status

**Phases 1–4** — Agent core complete.

**Phase 5** — Monorepo restructure: `apps/api`, `pocket-agent init`, Google OAuth + Worker → Pocket Node architecture documented. Next: load web/api templates and migrate off Supabase.
