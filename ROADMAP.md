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

Layout: workspace siblings `pocket-agent-web`, `pocket-agent-api`, `pocket-agent-desktop`, `pocket-agent-cli` + this repo's `src/pocket_agent`.


## 5.1 Monorepo scaffold

- [x] Sibling module layout and documentation
- [x] `pocket-agent init` — clone `pocket-agent-web-app` and `pocket-agent-api-app`
- [x] `pocket-agent-api/` scaffold for API worker template
- [x] `pocket-agent-cli/` placeholder for future CLI repo
- [x] [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md) — Google OAuth, Worker → Pocket Node, tunnel
- [x] `pocket-agent-desktop/` — empty scaffold for Tauri app


## 5.2 Web app (`pocket-agent-web`)

- [x] Direct Google OAuth (`@react-oauth/google`, no Supabase)
- [x] Cloudflare Pages deploy workflow (Google Client ID env)
- [x] Local dev against API worker → Pocket Node


## 5.3 API worker (`pocket-agent-api`) — Hono on Cloudflare Workers

- [x] Hono template in `pocket-agent-api`
- [x] Google ID token verification (shared Google Cloud client)
- [x] Proxy `POST /chat` to Pocket Node
- [x] Cloudflare Worker deploy workflow (`.github/workflows/api-worker-deploy.yml`)
- [x] Pocket Node tunnel URL via `POCKET_NODE_URL` secret (see `pocket-agent-api/docs/DEPLOYMENT.md`)


## 5.4 Desktop app (`pocket-agent-desktop`)

- [x] Tauri scaffold (embeds `pocket-agent-web` UI)
- [x] Google OAuth docs — [docs/GOOGLE_OAUTH.md](docs/GOOGLE_OAUTH.md) (web + Tauri dev origins)
- [x] Desktop build CI + icon script (`desktop-build.yml`, `scripts/generate-desktop-icons.sh`)
- [ ] Embedded local web UI + API worker / localhost agent (dev works via Vite)
- [ ] Optional: bundle Python agent in desktop installer


## 5.5 CLI (`pocket-agent-cli`)

- [x] `pocket-agent-cli` template in monorepo
- [x] Commands: `setup`, `profile`, `status`, `stack`
- [x] Shares `config/user-setup.yaml` with Python `pocket-agent setup`
- [ ] Deploy/install packaging (npm global, brew, bundled with desktop)


## 5.6 Shared client features

- [x] Monitoring view (`/monitor` — worker + Pocket Node status)
- [x] Connection profile badge in header (`VITE_CONNECTION_PROFILE`)
- [ ] Shared UI between web and desktop (web embedded in Tauri)
- [x] Environment config docs (setup wizard + `VITE_*` vars)


# Phase 6 - Advanced Automation

- [ ] Scheduled tasks
- [ ] Multi-agent workflows
- [ ] Personal automation recipes
- [ ] Plugin system
