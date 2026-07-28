# Agent & developer instructions — repo-name

**Hono + Supabase + Gemini** Cloudflare Worker API. Pairs with [paired-repo-name](https://github.com/owner-username/paired-repo-name).

## What ships out of the box

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /health` | Public | Liveness probe |
| `GET /me` | Bearer JWT | Authenticated user profile |
| `POST /chat` | Bearer JWT | `{ "message": "..." }` → Gemini reply |
| `GET /chat?message=` | Bearer JWT | Query-string Gemini prompt |

Set `GEMINI_API_KEY` in `.dev.vars` / Wrangler secrets. Details: [`index.md`](index.md)

## Local development

```bash
npm install
cp .env.example .dev.vars
npm run dev
```

## Deploy

See [`CLOUDFLARE_SETUP.md`](CLOUDFLARE_SETUP.md). Store `GEMINI_API_KEY` as a Wrangler secret in production.
