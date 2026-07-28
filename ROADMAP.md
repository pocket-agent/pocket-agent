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

Monorepo layout: `apps/web` (hosted) + `apps/desktop` (Tauri) + `src/pocket_agent` (agent core).


## 5.1 Monorepo scaffold

- [x] `apps/` layout and documentation
- [x] `apps/web/` — template loaded and initialized (`pocket-agent-web`)
- [x] `apps/desktop/` — empty scaffold for Tauri app


## 5.2 Web app (`apps/web`)

- [x] Copy Cloudflare + React + Google OAuth template into `apps/web/`
- [x] Run `init-from-template` (package `pocket-agent-web`, monorepo paths)
- [ ] Agent HTTP API for dashboard (status, files, memory, commands)
- [ ] Google OAuth (hosted and local redirect URLs)
- [ ] Cloudflare Pages deployment workflow
- [ ] Local static serve from Pocket Node (no Cloudflare required)


## 5.3 Desktop app (`apps/desktop`)

- [ ] Tauri scaffold (architecture copied from `apps/web`)
- [ ] macOS / Windows / Linux builds
- [ ] Embedded local web UI + localhost agent connection
- [ ] Optional: bundle Python agent in desktop installer


## 5.4 Shared client features

- [ ] Monitoring views (agent health, logs, queue)
- [ ] Shared UI components between web and desktop (as feasible)
- [ ] Environment config: local vs Cloudflare vs Tauri


# Phase 6 - Advanced Automation

- [ ] Scheduled tasks
- [ ] Multi-agent workflows
- [ ] Personal automation recipes
- [ ] Plugin system
