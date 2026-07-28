# Desktop app (`apps/desktop`)

**Tauri 2** shell that embeds the same UI as `apps/web` — Google OAuth, API worker or local agent.

## Status

**Scaffold** — wraps `apps/web` in a native window. No separate frontend; uses web Vite dev server in dev and `apps/web/dist` for release builds.

## Prerequisites

- [Rust](https://rustup.rs/)
- Bun (for `apps/web`)
- Same `GOOGLE_CLIENT_ID` as web (in `apps/web/.env.local`)

## Dev

```bash
# Start agent + API worker (optional for full stack)
pocket-agent serve
cd apps/api && npm run dev

# Desktop — starts web Vite then opens native window
cd apps/desktop
npm install
npm run dev
```

`tauri.conf.json` runs `bun run dev` in `apps/web` and loads `http://localhost:5173`.

Set `VITE_API_BASE_URL` in `apps/web/.env.local` (worker on `:8788` or direct agent on `:8787`).

## Release build

```bash
# Generate icons first (required for bundle)
cd apps/desktop
npx tauri icon ../../apps/web/src/assets/react-supabase-auth-template-logo.png

npm run build
```

Installers output under `src-tauri/target/release/bundle/`.

## Architecture

| Mode | UI | API |
|------|-----|-----|
| Dev | Vite `:5173` in Tauri webview | Local worker or agent |
| Release | Built `apps/web/dist` | User-configured URL |

Same Google OAuth client ID as web — add desktop redirect URIs in Google Cloud when using OAuth in the packaged app.

## Deploy

Desktop install only — not deployed to Cloudflare.

## Layout

```
apps/desktop/
├── package.json
├── src-tauri/
│   ├── tauri.conf.json
│   ├── src/main.rs
│   └── capabilities/
└── (UI from apps/web)
```

Docs: [../../docs/APPS_ARCHITECTURE.md](../../docs/APPS_ARCHITECTURE.md)
