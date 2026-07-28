# Pocket Agent Roadmap


# Phase 1 - Foundation

- [x] Python project structure
- [x] Telegram bot
- [x] Gemini integration
- [x] Configuration system
- [x] NAS folder access


# Phase 2 - File Intelligence

- [x] File indexing
- [x] Search system
- [x] PDF extraction
- [x] Document parsing
- [x] Spreadsheet analysis


# Phase 3 - Safe Editing

- [x] Excel editing
- [x] PDF editing
- [x] Word editing
- [x] Backup system
- [x] Validation system


# Phase 4 - Memory

- [x] Personal memory
- [x] Vector search
- [x] Knowledge base
- [x] Skill retrieval


# Phase 5 - Clients (monorepo)

Layout: `apps/web` + `apps/api` + `apps/desktop` + `apps/cli` + `src/pocket_agent`.


## 5.1 Monorepo scaffold

- [x] `apps/` layout and documentation
- [x] `pocket-agent init` — clone `pocket-agent-web-app` and `pocket-agent-api-app`
- [x] `apps/api/` scaffold for API worker template
- [x] `apps/cli/` placeholder for future CLI repo
- [x] [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md) — Google OAuth, Worker → Pocket Node, tunnel
- [x] `apps/desktop/` — empty scaffold for Tauri app


## 5.2 Web app (`apps/web`)

- [x] Direct Google OAuth (`@react-oauth/google`, no Supabase)
- [x] Cloudflare Pages deploy workflow (Google Client ID env)
- [x] Local dev against API worker → Pocket Node


## 5.3 API worker (`apps/api`) — Hono on Cloudflare Workers

- [x] Hono template in `apps/api`
- [x] Google ID token verification (shared Google Cloud client)
- [x] Proxy `POST /chat` to Pocket Node
- [x] Cloudflare Worker deploy workflow (`.github/workflows/api-worker-deploy.yml`)
- [x] Pocket Node tunnel URL via `POCKET_NODE_URL` secret (see `apps/api/docs/DEPLOYMENT.md`)


## 5.4 Desktop app (`apps/desktop`)

- [x] Tauri scaffold (embeds `apps/web` UI)
- [ ] Same Google OAuth client ID — desktop redirect URIs in Google Cloud
- [ ] macOS / Windows / Linux release builds (icons + CI)
- [ ] Embedded local web UI + API worker / localhost agent
- [ ] Optional: bundle Python agent in desktop installer


## 5.5 CLI (`apps/cli`)

- [ ] Enable in `config/apps.yaml` when `pocket-agent-cli` is ready
- [ ] Desktop install only (no Cloudflare deploy)


## 5.6 Shared client features

- [ ] Monitoring views (agent health, logs, queue)
- [ ] Shared UI between web and desktop (as feasible)
- [ ] Environment config: local vs Cloudflare vs Tauri vs CLI


# Phase 6 - Advanced Automation

- [ ] Scheduled tasks
- [ ] Multi-agent workflows
- [ ] Personal automation recipes
- [ ] Plugin system
