# API app (`apps/api`)

Placeholder for **pocket-agent-api-app** — Cloudflare Worker that validates Google OAuth tokens and proxies requests to your **Pocket Node** (local Python agent).

## Status

**Empty scaffold** — load your template here, or clone the official repo:

```bash
pocket-agent init --only api
# or from repo root:
./scripts/init-apps.sh api
```

Repository: [pocket-agent/pocket-agent-api-app](https://github.com/pocket-agent/pocket-agent-api-app)

## Role in the stack

| Layer | Deploy target | Responsibility |
|-------|---------------|----------------|
| `apps/web` | Cloudflare Pages | React UI, Google Client ID in browser |
| `apps/api` | Cloudflare Worker | Verify Google tokens, route to Pocket Node |
| `src/pocket_agent` | Pocket Node (local) | LLM keys, tools, files, memory |

The browser never holds LLM API keys. OAuth identifies the user; the worker forwards actions to the agent (local dev or via **Cloudflare Tunnel** in production).

## Nested git

Like `apps/web`, this folder is its own git repository after clone. Commit and push from `apps/api/`, not from the monorepo root for app-specific changes.

## Docs

- [docs/APPS_ARCHITECTURE.md](../../docs/APPS_ARCHITECTURE.md)
- [apps/README.md](../README.md)
