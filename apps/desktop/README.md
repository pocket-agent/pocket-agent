# Desktop app (`apps/desktop`)

Placeholder for the **Tauri** multi-platform desktop application.

## Plan

1. Complete `apps/web` with the Cloudflare/React/OAuth template.
2. Copy the initial UI architecture from `apps/web` into this Tauri project.
3. Embed the web UI in a native shell (macOS, Windows, Linux).

## Local-first

Desktop installs bundle the agent and UI on the same machine — no Cloudflare required. The Tauri app loads the local web build or dev server and connects to the Python agent on localhost.

## Expected layout (after scaffold)

```
apps/desktop/
├── src-tauri/     # Tauri Rust backend
├── src/           # Frontend (mirrored from apps/web)
└── package.json
```

## Status

**Empty scaffold** — Tauri project will be added after the web template lands.
