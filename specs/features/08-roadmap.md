---
type: Playbook
title: Roadmap
description: Phased delivery plan from foundation through advanced automation.
tags: [roadmap]
timestamp: 2026-07-28T00:00:00Z
---

Phased delivery. Track progress in [ROADMAP.md](../../ROADMAP.md).

## Phase 1 — Foundation

- Python project structure
- Telegram bot
- Gemini integration
- Configuration system
- NAS folder access

## Phase 2 — File intelligence

- File indexing
- Search system
- PDF extraction
- Document parsing
- Spreadsheet analysis

## Phase 3 — Safe editing

- Excel editing
- PDF editing
- Word editing
- Backup system
- Validation system

## Phase 4 — Memory

- Personal memory
- Vector search
- Knowledge base
- Skill retrieval

## Phase 5 — Clients (monorepo)

### 5.1 Scaffold

- `apps/` layout (`apps/web`, `apps/desktop`)
- Documentation for local vs Cloudflare deployment

### 5.2 Web (`apps/web`)

- Cloudflare + React + Google OAuth template
- Agent HTTP API
- Local static serve on Pocket Node
- Cloudflare Pages deployment

### 5.3 Desktop (`apps/desktop`)

- Tauri scaffold from web architecture
- Multi-platform builds
- Localhost agent connection

### 5.4 Shared

- Monitoring views
- OAuth across hosted and local modes

## Phase 6 — Advanced automation

- Scheduled tasks
- Multi-agent workflows
- Personal automation recipes
- Plugin system

## Spec linkage

When a phase item ships, update the matching feature spec under `specs/features/` and add an entry to [CHANGELOG.md](../../CHANGELOG.md).
