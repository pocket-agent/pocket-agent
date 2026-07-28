# Desktop app (`apps/desktop`)

Placeholder for the **Tauri** multi-platform desktop application.

## Plan

1. Complete `apps/web` (`pocket-agent-web-app`) with direct Google OAuth.
2. Copy UI architecture from web into this Tauri project.
3. Use the **same Google Cloud OAuth client ID** as the web app.
4. Connect to the API worker (hosted) or local agent on desktop.

## Local-first

Desktop installs bundle the agent and UI on the same machine. The Tauri app calls the API worker or `pocket-agent serve` on localhost — no Cloudflare required for offline use.

## Deploy

Desktop install only — not deployed to Cloudflare (unlike `apps/web` and `apps/api`).

## Expected layout (after scaffold)

```
apps/desktop/
├── src-tauri/     # Tauri Rust backend
├── src/           # Frontend (mirrored from apps/web)
└── package.json
```

## Status

**Empty scaffold** — Tauri project will be added after the web template lands.
