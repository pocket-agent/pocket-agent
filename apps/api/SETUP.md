# Setup

## Supabase

1. Create a project at [supabase.com](https://supabase.com).
2. Under **Project Settings → API**, copy:
   - Project URL → `SUPABASE_URL`
   - `anon` public key → `SUPABASE_ANON_KEY`
   - `service_role` key → `SUPABASE_SERVICE_ROLE_KEY` (server only; never expose to the browser)

No custom SQL migrations are required for the default `GET /me` endpoint—it uses Supabase Auth only.

### Google OAuth (for the React frontend)

Configure Google as an OAuth provider in **Authentication → Providers** in the Supabase dashboard. Redirect URLs must include your frontend origin (e.g. `http://localhost:5173` for local dev). See the React template's `docs/SUPABASE_SETUP.md` for step-by-step UI setup.

## Local worker secrets

Wrangler reads secrets from `.dev.vars` (gitignored):

```bash
cp .env.example .dev.vars
# edit values
npm run dev
```

## CORS

Set `ALLOWED_ORIGINS` to a comma-separated list of frontend origins:

```bash
ALLOWED_ORIGINS=http://localhost:5173,https://your-app.pages.dev
```

If unset, the worker allows the request origin (suitable for local development only).

## Production

Use `wrangler secret put` for each variable—see [`CLOUDFLARE_SETUP.md`](CLOUDFLARE_SETUP.md).

## Adding database features later

When you add tables:

1. Create migrations in Supabase.
2. Add Zod schemas under `src/schemas/`.
3. Add route handlers under `src/routes/`.
4. Use `getSupabaseClientWithJWT` so Row Level Security applies to the authenticated user.
5. Update `index.md` with new endpoints.
