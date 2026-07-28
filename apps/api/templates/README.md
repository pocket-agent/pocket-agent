# repo-name

Cloudflare Worker API with **Hono**, **Supabase Auth**, and **Google Gemini**. Pairs with [paired-repo-name](https://github.com/owner-username/paired-repo-name).

## Out-of-the-box features

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /health` | Public | Liveness check |
| `GET /me` | Bearer JWT | Authenticated user profile |
| `POST /chat` | Bearer JWT | JSON body `{ "message": "..." }` → Gemini reply |
| `GET /chat?message=` | Bearer JWT | Query-string Gemini prompt |

See [`index.md`](index.md).

## Quick start

```bash
npm install
cp .env.example .dev.vars
npm run dev
```

## Environment variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes | Anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Service role key |
| `GEMINI_API_KEY` | Yes | Google AI Studio API key |
| `GEMINI_MODEL` | No | Model override (default `gemini-2.5-flash`) |
| `ALLOWED_ORIGINS` | No | CORS origins |

Maintained by [author-display-name](https://github.com/author-github-login).

## License

MIT
