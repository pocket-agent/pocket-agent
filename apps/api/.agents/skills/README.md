# cf-hono-supabase-gemini-api-template — Agent Skills Index

Skills teach agents how this Cloudflare Worker API works and how to extend it safely.

## Project status (current template)

**Hono + Supabase + Gemini** worker paired with **react-supabase-auth-ai-chat-template**:

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /health` | Public | Liveness check |
| `GET /me` | Bearer JWT | Current user via `auth.getUser()` |
| `POST /chat` | Bearer JWT | Gemini chat completion (`message`, optional `history`) |
| `GET /chat?message=` | Bearer JWT | Query alternative for quick tests (no history) |

Requires `GEMINI_API_KEY` (and optional `GEMINI_MODEL`) for chat. No custom Postgres tables for the default template.

Canonical OKF specs: [`index.md`](../../index.md) · OKF modules: [`.agents/skills/index.md`](index.md)

## Cursor SKILL.md packs

| Skill | Use when |
|-------|----------|
| [create-api-endpoint](create-api-endpoint/SKILL.md) | Adding routes, registering routers, public vs protected endpoints |
| [create-zod-schema](create-zod-schema/SKILL.md) | Request/response validation with Zod |
| [authentication](authentication/SKILL.md) | JWT middleware, Supabase client selection, `/me` patterns |
| [supabase-mcp](supabase-mcp/SKILL.md) | Migrations, seeding, schema inspection via Supabase MCP |

### Upstream Supabase skills (optional install)

[`skills-lock.json`](../../skills-lock.json) pins `supabase/agent-skills` versions (not tied to any MCP `project_ref`).

```bash
npx skills add supabase/agent-skills --skill supabase
npx skills add supabase/agent-skills --skill supabase-postgres-best-practices
```

Or configure Supabase MCP in Cursor (see `INSTRUCTIONS.md`).

## OKF modules (local)

| Module | Use when |
|--------|----------|
| [auth-middleware](modules/auth-middleware.md) | Hono JWT gate and client selection |
| [chat-route](modules/chat-route.md) | `POST/GET /chat` handlers and Gemini wiring |
| [gemini-client](modules/gemini-client.md) | `@google/genai` wrapper and env vars |

Shared concepts (synced): [shared/auth/](shared/auth/) · [shared/supabase/](shared/supabase/)

## Project layout

```
src/
├── index.ts           # Route registration, middleware order
├── routes/
│   ├── health.ts      # Public
│   ├── me.ts          # Protected
│   └── chat.ts        # Protected — Gemini
├── middleware/        # auth, CORS, errors
├── lib/               # supabase.ts, gemini.ts
├── utils/             # jwt, auth, response
└── schemas/           # Zod schemas (add as needed)
```

## Extension order

1. **Schema** (if validating body/query) → `src/schemas/`
2. **Route** → `src/routes/<name>.ts`
3. **Register** in `src/index.ts` (public before auth, or after `authMiddleware`)
4. **Migration** (if new tables) → Supabase MCP / CLI; enable RLS
5. **Document** → `specs/features/` + `.agents/skills/modules/` + frontend `src/api/` module

## Middleware order (do not break)

```
logger → cors → errorHandler → /health (public) → authMiddleware → protected routes
```

## Environment

Local: `.dev.vars` (from `.env.example`). Production: `wrangler secret put`.

Required: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`. Optional: `ALLOWED_ORIGINS`, `GEMINI_MODEL`.
