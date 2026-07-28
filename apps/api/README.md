# Pocket Agent API (`apps/api`)

Hono **Cloudflare Worker** — validates **Google OAuth ID tokens** (JWT) and will proxy to the Pocket Node Python agent.

Monorepo: [../../README.md](../../README.md) · Architecture: [../../docs/APPS_ARCHITECTURE.md](../../docs/APPS_ARCHITECTURE.md)

## Auth (no Supabase)

1. Web/desktop sign in with **Google** using `GOOGLE_CLIENT_ID` in the frontend.
2. Frontend sends `Authorization: Bearer <google_id_token>` on API calls.
3. Worker verifies the JWT with [Google's JWKS](https://www.googleapis.com/oauth2/v3/certs) and checks `aud` matches `GOOGLE_CLIENT_ID`.

## Enabled routes

| Route | Auth | Description |
|-------|------|-------------|
| `GET /health` | No | Liveness |
| `GET /auth` | Google JWT | Token valid + minimal identity |
| `GET /me` | Google JWT | Profile from token claims |
| `POST /chat` | Google JWT | Proxy to Pocket Node (`POCKET_NODE_URL`) |

## Local dev

```bash
cp .env.example .dev.vars
# Set GOOGLE_CLIENT_ID (same as web app)
npm install
npm run dev
```

Default worker port is often `8787` — use `8788` in `config/user-setup.yaml` if the agent also uses `8787`:

```bash
wrangler dev --port 8788
```

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | Google Cloud OAuth client ID (shared with web/Tauri) |
| `ALLOWED_ORIGINS` | No | CORS origins (comma-separated) |
| `POCKET_NODE_URL` | No | Pocket Node URL when proxy routes are enabled |

Deploy secrets: `wrangler secret put GOOGLE_CLIENT_ID`

## Frontend contract

Store the Google **ID token** as `localStorage['x-auth-token']` (same key as the web template) so `apiFetch` attaches it as Bearer JWT.

## Nested git

This folder is a separate git repo inside the monorepo.
