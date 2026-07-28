# Pocket Agent monorepo apps

Client applications live under `apps/`. Each app is a **nested git repository** (clone with `pocket-agent init`).

| Path | Package repo | Deploy |
|------|--------------|--------|
| [`web/`](web/) | [pocket-agent-web-app](https://github.com/pocket-agent/pocket-agent-web-app) | Cloudflare Pages |
| [`api/`](api/) | [pocket-agent-api-app](https://github.com/pocket-agent/pocket-agent-api-app) | Cloudflare Worker |
| [`desktop/`](desktop/) | (Tauri — scaffold) | Desktop install |
| [`cli/`](cli/) | [pocket-agent-cli](https://github.com/pocket-agent/pocket-agent-cli) | Desktop install (future) |

Python agent core: [`src/pocket_agent/`](../src/pocket_agent/) · Runtime assets: [`agent/`](../agent/)

## Architecture

**Google OAuth** (single Google Cloud client ID) on web and desktop — **no Supabase**.

- **Web** (Pages) → **API worker** → **Pocket Node** (`pocket-agent serve`, optionally via Cloudflare Tunnel)
- LLM keys and tools stay on the Pocket Node; the browser never calls external LLM APIs directly.

Full diagram: [docs/APPS_ARCHITECTURE.md](../docs/APPS_ARCHITECTURE.md)

## First-time setup

```bash
pip install -e ".[dev]"
pocket-agent init              # clone web + api repos into apps/
# or
./scripts/init-apps.sh
```

| Command | Action |
|---------|--------|
| `pocket-agent init` | Clone all enabled apps from `config/apps.yaml` |
| `pocket-agent init --only api` | Clone only the API worker repo |
| `pocket-agent init --only web` | Clone only the web app (skips if `apps/web` is already populated) |
| `pocket-agent init --force` | Replace scaffold directories (destructive) |

Repos are defined in [`config/apps.yaml`](../config/apps.yaml).

## `apps/web`

React dashboard — Google OAuth in the browser, calls the API worker.

```bash
cd apps/web && bun install && bun run dev
```

## `apps/api`

Cloudflare Worker — verifies Google tokens, proxies chat/actions to your Pocket Node.

```bash
cd apps/api && npm install && npm run dev   # after template is loaded
```

**Empty scaffold** until you add a template or run `pocket-agent init --only api`.

## `apps/desktop`

Tauri shell (future) — same Google OAuth client as web, connects to API worker or local agent.

## `apps/cli`

Terminal client (future) — `enabled: false` in `config/apps.yaml` until the CLI repo is ready.

## Deployment summary

| Target | What |
|--------|------|
| Cloudflare Pages | `apps/web` |
| Cloudflare Worker | `apps/api` |
| Pocket Node | `pocket-agent serve` + optional `cloudflared` tunnel |
| Desktop | Tauri + CLI — local install only |

## Nested git

`apps/web` and `apps/api` are separate git projects. Work inside each app directory for app-specific commits. The monorepo root tracks agent core, config, and scaffolding.
