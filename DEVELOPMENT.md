# Pocket Agent — Development

Setup, monorepo layout, testing, and deployment.

## Requirements

- Python 3.12+ (agent core)
- Node.js 20+ (when `apps/web` and `apps/desktop` are populated)
- Telegram bot token, Gemini API key (see `.env.example`)
- NAS mount or local folder for development

## Monorepo layout

```
pocket-agent/
├── apps/
│   ├── web/          # React + Cloudflare + Google OAuth (template → you add)
│   └── desktop/      # Tauri app (scaffold from web, later)
├── src/pocket_agent/ # Python agent (Telegram, tools, memory)
├── agent/            # Runtime skills & prompts
├── config/           # YAML config
├── data/             # Runtime logs, cache, working files
└── tests/            # pytest
```

See [apps/README.md](apps/README.md) for client app details.

## Agent quick start

```bash
cd pocket-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # configure tokens and keys
pocket-agent           # Telegram bot
```

## Web app

```bash
cd apps/web
bun install
cp .env.example .env.local
bun run dev
```

See [apps/web/README.md](apps/web/README.md) and [apps/web/MONOREPO.md](apps/web/MONOREPO.md).

Remove nested git if present: `rm -rf apps/web/.git`

**Local Pocket Node:** build `apps/web` and serve via agent HTTP (Phase 5.2) — no Cloudflare required.

**Hosted:** deploy `apps/web` to Cloudflare Pages.

## Desktop app (later)

```bash
cd apps/desktop
# Tauri dev/build after scaffold from apps/web
```

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
- [INSTRUCTIONS.md](INSTRUCTIONS.md)
- [specs/features/](specs/features/)
- [apps/README.md](apps/README.md)

## Status

**Phases 1–4** — Agent core complete (see [ROADMAP.md](ROADMAP.md)).

**Phase 5** — Monorepo scaffold ready. Next: copy web template into `apps/web/`, then Tauri scaffold in `apps/desktop/`.
