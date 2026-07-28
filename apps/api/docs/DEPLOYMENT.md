# Pocket Agent API — Cloudflare Workers deployment

Hono worker: Google JWT verification + proxy to Pocket Node.

## Prerequisites

- Cloudflare account
- `wrangler login` or `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` for CI
- Google OAuth client ID (same as `apps/web`)
- Pocket Node reachable at a URL (local dev or **Cloudflare Tunnel** in production)

## One-time secrets (production)

From `apps/api`:

```bash
wrangler secret put GOOGLE_CLIENT_ID --env production
wrangler secret put POCKET_NODE_URL --env production
wrangler secret put ALLOWED_ORIGINS --env production
```

| Secret | Example | Purpose |
|--------|---------|---------|
| `GOOGLE_CLIENT_ID` | `123...apps.googleusercontent.com` | Verify Google ID tokens |
| `POCKET_NODE_URL` | `https://agent.yourdomain.com` | Tunnel/nginx URL to `pocket-agent serve` |
| `ALLOWED_ORIGINS` | `https://pocket-agent-web.pages.dev` | CORS for web app |

`GOOGLE_CLIENT_ID` is public in the browser but stored as a Worker secret/env for server verification.

## Pocket Node + Cloudflare Tunnel (production)

On your home/NAS machine:

```bash
# 1. Agent
GOOGLE_CLIENT_ID=your-client-id
pocket-agent serve

# 2. Tunnel (example — expose local :8787)
cloudflared tunnel --url http://127.0.0.1:8787
```

Use the tunnel HTTPS URL as `POCKET_NODE_URL` in the Worker.

Flow: **Pages (web)** → **Worker (API)** → **Tunnel** → **Pocket Node (agent)**

## Deploy manually

```bash
cd apps/api
npm ci
npm run type-check
wrangler deploy --env production
```

## GitHub Actions

Monorepo workflow: [`.github/workflows/api-worker-deploy.yml`](../../../.github/workflows/api-worker-deploy.yml)

**Repository secrets:** `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`

Secrets above must still be set in Cloudflare (`wrangler secret put`) — CI deploys code, not tunnel URLs.

## Custom domain (optional)

Add to `wrangler.toml`:

```toml
[env.production]
routes = [
  { pattern = "api.yourdomain.com/*", custom_domain = true }
]
```

Point `VITE_API_BASE_URL` in Pages to `https://api.yourdomain.com`.

## Local dev

```bash
cp .env.example .dev.vars
npm run dev   # :8788, proxies to POCKET_NODE_URL
```

## Related

- [README.md](../README.md)
- [../../docs/APPS_ARCHITECTURE.md](../../docs/APPS_ARCHITECTURE.md)
- [Web Pages deploy](../../../.github/workflows/web-pages-deploy.yml)
