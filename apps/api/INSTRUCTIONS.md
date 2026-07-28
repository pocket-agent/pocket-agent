# Agent & developer instructions — cf-hono-supabase-gemini-api-template

Use this file when turning this template into a **production API** on Cloudflare Workers. This repository is **self-contained**; you do not need the frontend template to run the worker, but pairing with [react-supabase-auth-template](https://github.com/open-templates/react-supabase-auth-template) is the recommended demo for end-to-end auth.

## What ships out of the box

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /health` | Public | Liveness check |
| `GET /me` | Bearer JWT | Current Supabase user |
| `POST /chat` | Bearer JWT | `{ "message": "..." }` → Gemini reply |
| `GET /chat?message=` | Bearer JWT | Query-string Gemini prompt |

Details: [`index.md`](index.md)

---

## Prerequisites (required before development)

### 1. Supabase project

1. Create a project at [supabase.com](https://supabase.com).
2. From **Settings → API**, copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` (server only; never commit or expose to browsers)

No custom database tables are required for the default `/me` endpoint (Supabase Auth only). Add migrations when you extend the API with Postgres data.

### 2. Cloudflare account (for deploy)

- [Cloudflare Workers](https://developers.cloudflare.com/workers/) account
- Wrangler CLI: `npm install -g wrangler` or use project devDependency

Local development does not require Cloudflare login if you use `wrangler dev` with local secrets.

---

## Setup checklist

```bash
npm install
cp .env.example .dev.vars
# Edit .dev.vars with Supabase credentials and GEMINI_API_KEY
npm run dev   # http://localhost:8787
```

Verify:

```bash
curl http://localhost:8787/health
curl -H "Authorization: Bearer <supabase-access-token>" http://localhost:8787/me
curl -X POST http://localhost:8787/chat \
  -H "Authorization: Bearer <supabase-access-token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Gemini"}'
```

Full guides: [`QUICKSTART.md`](QUICKSTART.md), [`SETUP.md`](SETUP.md), [`CLOUDFLARE_SETUP.md`](CLOUDFLARE_SETUP.md)

### Environment variables

| Variable | Required | Notes |
|----------|----------|-------|
| `SUPABASE_URL` | Yes | |
| `SUPABASE_ANON_KEY` | Yes | Used with user JWT |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Admin operations only |
| `GEMINI_API_KEY` | Yes | [Google AI Studio](https://aistudio.google.com/apikey) — server only |
| `GEMINI_MODEL` | No | Default `gemini-2.5-flash` |
| `ALLOWED_ORIGINS` | Recommended | Comma-separated frontend origins for CORS |
| `ENVIRONMENT` | No | `development` / `staging` / `production` |

Production: set via `wrangler secret put` (see `CLOUDFLARE_SETUP.md`).

---

## Connecting the frontend (missing piece for full stack)

This worker does **not** include a UI. To test auth end-to-end:

1. Clone or fork **[react-supabase-auth-template](https://github.com/open-templates/react-supabase-auth-template)**.
2. Complete **its** `INSTRUCTIONS.md` (Supabase + Google OAuth + redirect URLs).
3. In the frontend `.env.local`:
   ```bash
   VITE_API_BASE_URL=http://localhost:8787   # or your deployed worker URL
   ```
4. Set worker `ALLOWED_ORIGINS` to the frontend origin (e.g. `http://localhost:5173`).
5. Run both: worker `npm run dev`, frontend `bun run dev`.

The frontend sends `Authorization: Bearer <token>` from Supabase session; this worker validates it on protected routes.

---

## Agent workflow (extending to production)

Read in order:

1. **`INSTRUCTIONS.md`** (this file) — prerequisites and pairing
2. **`index.md`** — current API contract
3. **`.agents/skills/index.md`** — OKF module guides
4. **`.agents/skills/README.md`** — Cursor `SKILL.md` catalog
5. **`skills-lock.json`** — pinned upstream Supabase skills (optional `npx skills add` to install)

### Supabase MCP vs skills-lock

| | **Cursor MCP** (`~/.cursor/mcp.json`) | **`skills-lock.json`** |
|---|---|---|
| Purpose | Connect agent to *your* Supabase project at runtime | Pin *public* skill packs from `supabase/agent-skills` |
| Personal? | Yes — `project_ref` is per developer/project | No — same hashes for everyone on the same skill version |

Configure MCP separately after clone; it is not stored in this repository.

### Adding a new endpoint

1. **Database** (if needed): use Supabase MCP / CLI — see `.agents/skills/supabase-mcp/SKILL.md`
2. **Zod schema** (if validating input): `src/schemas/` — see `create-zod-schema` skill
3. **Route**: `src/routes/` — see `create-api-endpoint` skill
4. **Register** in `src/index.ts` (public routes before `authMiddleware`)
5. **Document** in `index.md`
6. **Frontend** (if UI consumes it): add module in react template `src/api/`

### Rules

- Prefer `getSupabaseClientWithJWT` over service role for user data (RLS).
- Use `successResponse` / `errorResponse` from `src/utils/response.ts`.
- Never expose `SUPABASE_SERVICE_ROLE_KEY` to clients.
- Run `npm run type-check` before finishing.

---

## Repository map

```
src/index.ts          Entry + middleware order
src/routes/           health.ts, me.ts (+ your routes)
src/middleware/       Auth, CORS, errors
src/lib/supabase.ts   Client factories
index.md     Feature specification
skills-lock.json        Pinned upstream Supabase agent skills
.agents/skills/         Project agent skills
.cursor/rules/        Cursor IDE rules
```

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| `401` on `/me` | Valid Supabase access token; `SUPABASE_URL` / keys match frontend project |
| CORS errors | `ALLOWED_ORIGINS` includes exact frontend origin |
| Frontend shows API offline | Worker running; correct `VITE_API_BASE_URL` |

---

## License

MIT — see `LICENSE`.
