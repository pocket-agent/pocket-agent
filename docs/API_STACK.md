# API stack decision — use Hono (TypeScript)

Recommendation for `apps/api` (**pocket-agent-api-app**): **Hono on Cloudflare Workers**, with `wrangler dev` for local development.

## Short answer

| Template | Verdict |
|----------|---------|
| **Hono.js** | **Use this** — Workers-native, local/prod parity, thin proxy, same TS ecosystem as web |
| **FastAPI** | Avoid for this layer — not a Workers runtime; needs Containers or a separate host |
| **Rust (workers-rs)** | Valid but secondary — more complexity, little benefit for an auth + proxy gateway |

Put your Hono-based Cloudflare template into `apps/api`.

## What `apps/api` actually does

It is **not** the brain. It is an **edge gateway**:

```
Frontend (web / Tauri)
    → Google OAuth token in browser
    → apps/api (verify token, CORS, routing)
    → Pocket Node OR (optional) cloud LLM APIs
```

| Responsibility | Where it lives |
|----------------|----------------|
| UI, Google Client ID | `apps/web`, `apps/desktop` |
| Verify Google tokens, CORS, route requests | `apps/api` (Hono Worker) |
| Tools, files, NAS, memory, LLM keys (default) | `src/pocket_agent` (Pocket Node) |
| Expose home agent to internet | `cloudflared` / nginx (on Pocket Node) |

### Two routing modes (configured per user, not hard-coded in one app)

| Mode | API worker behavior | LLM keys |
|------|---------------------|----------|
| **Pocket Node** (default) | Proxy `/health`, `/me`, `/chat` → `http://127.0.0.1:8787` or tunnel URL | On Pocket Node only |
| **Cloud relay** (no local agent) | Worker calls Gemini/OpenAI directly — chat only, no NAS/tools | Worker secrets (Wrangler) |

Default first-time setup: **Pocket Node mode, all local**. Cloud relay is opt-in for users without a home server.

The worker should stay thin in Pocket Node mode: no duplicate tool/memory logic.

## Why not FastAPI?

| Issue | Detail |
|-------|--------|
| Workers runtime | FastAPI is Python/WSGI — it does **not** run on standard Workers |
| Cloudflare option | **Workers Containers** (Docker) — heavier, different deploy, worse cold starts |
| Local vs prod | `uvicorn` locally ≠ Workers in production — two environments to maintain |
| Monorepo fit | Python agent already owns execution; another Python service adds overlap |

FastAPI is excellent for a **self-hosted API on the Pocket Node** — that role is already `pocket-agent serve`. A second Python API on Cloudflare duplicates that without Workers-native deploy.

## Why not Rust?

| Pros | Cons |
|------|------|
| Fast on Workers | Separate language from web (React/TS) and agent (Python) |
| Small bundles | Slower iteration for a simple proxy |
| Strong security story | OAuth + `fetch()` proxy is not CPU-bound |

Choose Rust later only if you need Workers-specific primitives (Durable Objects, complex edge logic) at scale. For v1 gateway, Hono is enough.

## Why Hono wins

1. **Same deploy target locally and in production** — `wrangler dev` uses the Workers runtime locally.
2. **Designed for Workers** — Hono is the common choice for CF Workers + Pages Functions.
3. **TypeScript alignment** — shared API types/contracts with `apps/web`; future shared package `@pocket-agent/contracts`.
4. **Thin proxy is trivial**:

```ts
app.post('/chat', async (c) => {
  await verifyGoogleToken(c.req.header('Authorization'));
  const pocketUrl = c.env.POCKET_NODE_URL; // tunnel or http://127.0.0.1:8787
  return fetch(`${pocketUrl}/chat`, { method: 'POST', body: c.req.raw.body, headers: ... });
});
```

5. **You already have a Hono + CF template lineage** — fastest path to `pocket-agent-api-app`.

## Connection profiles (web / Tauri / CLI)

Users pick a **profile** (CLI/desktop wizard later; defaults on first init):

| Profile | Web | API | Agent | Typical user |
|---------|-----|-----|-------|--------------|
| **all-local** (default) | Vite dev / local build | `wrangler dev` | `pocket-agent serve` | First download, developers |
| **local-ui-remote-api** | local | deployed Worker URL | tunnel → home | Dev UI against prod worker |
| **hosted-ui-home-agent** | Pages | deployed Worker | tunnel → home | Production |
| **cloud-only** | Pages | deployed Worker (cloud LLM mode) | none | No Pocket Node |

Tauri/CLI responsibilities:

- Switch profile (`config/user-setup.yaml`)
- Start/stop local stack (`serve`, `wrangler dev`, `cloudflared`)
- Deploy worker/Pages from desktop (`wrangler deploy`)
- Register tunnel URL with worker secrets

## First-time init default

`pocket-agent setup` writes `config/user-setup.yaml` with **`profile: all-local`**. See `config/setup.defaults.yaml`.

```yaml
profile: all-local
web:
  mode: local          # vite dev → http://localhost:5173
api:
  mode: local          # wrangler dev → http://localhost:8787 (or separate port)
agent:
  mode: local          # pocket-agent serve
  url: http://127.0.0.1:8787
routing:
  llm: pocket_node     # pocket_node | cloud_relay
```

## Local dev ports (suggested)

| Service | Port | Command |
|---------|------|---------|
| Agent (Pocket Node) | `8787` | `pocket-agent serve` |
| API Worker (Hono) | `8788` | `wrangler dev` in `apps/api` |
| Web (Vite) | `5173` | `bun run dev` in `apps/web` |

Web `VITE_API_BASE_URL` → `http://localhost:8788` (worker), worker `POCKET_NODE_URL` → `http://127.0.0.1:8787` (agent).

## Related

- [APPS_ARCHITECTURE.md](APPS_ARCHITECTURE.md)
- [apps/api/README.md](../apps/api/README.md)
- `config/setup.defaults.yaml`
