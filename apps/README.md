# Pocket Agent monorepo

Pocket Agent is a monorepo: Python agent core plus client applications.

| Path | Role |
|------|------|
| [`src/pocket_agent/`](../src/pocket_agent/) | Python agent — Telegram, tools, memory, LLM routing |
| [`agent/`](../agent/) | Runtime skills, prompts, memory data |
| [`apps/web/`](web/) | **pocket-agent-web** — React, Supabase Auth, Cloudflare Pages, Google OAuth |
| [`apps/desktop/`](desktop/) | Tauri desktop app (scaffold pending) |
| [`config/`](../config/) | Shared YAML configuration |
| [`tests/`](../tests/) | Python test suite |

## Web app (`apps/web`)

Initialized from the React + Supabase + AI chat template. Run from `apps/web`:

```bash
bun install
cp .env.example .env.local
bun run dev
```

See [web/README.md](web/README.md) and [web/MONOREPO.md](web/MONOREPO.md).

**Note:** If `apps/web/.git` exists (nested clone), remove it so the monorepo root is the only git root:

```bash
rm -rf apps/web/.git
```

## Deployment modes

**Pocket Node (local):** Agent + built web UI on the same machine (Phase 5).

**Cloudflare Pages:** Deploy `apps/web` (build: `bun run ci`, root: `apps/web`).

**Desktop:** `apps/desktop` Tauri shell (later).

## Phase 5

See [ROADMAP.md](../ROADMAP.md).
