# Quick start

## 1. Prerequisites

- Node.js 18+
- A [Supabase](https://supabase.com) project (Auth enabled)
- A [Google AI Studio](https://aistudio.google.com/apikey) API key for Gemini
- [Wrangler](https://developers.cloudflare.com/workers/wrangler/) CLI

## 2. Install

```bash
npm install
cp .env.example .dev.vars
```

Edit `.dev.vars`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GEMINI_API_KEY=your-gemini-api-key
ALLOWED_ORIGINS=http://localhost:5173
ENVIRONMENT=development
# Optional: override the default model (gemini-2.5-flash)
# GEMINI_MODEL=gemini-2.5-flash
```

## 3. Run locally

```bash
npm run dev
```

Worker listens at `http://localhost:8787`.

## 4. Verify

```bash
# Health (public)
curl http://localhost:8787/health

# Me (requires a Supabase access token from a signed-in user)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8787/me

# Gemini — POST with JSON body (Bearer token required)
curl -X POST http://localhost:8787/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain JWT auth in one sentence."}'

# Gemini — GET with query string (same auth)
curl -G http://localhost:8787/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --data-urlencode "message=Hello from curl"
```

Get a token from the React app after login (`localStorage.getItem('x-auth-token')`) or from Supabase Auth APIs during development.

Example success response from `/chat`:

```json
{
  "success": true,
  "data": {
    "message": "Explain JWT auth in one sentence.",
    "reply": "...",
    "model": "gemini-2.5-flash"
  }
}
```

## 5. Pair with the React frontend

1. Start this worker (`npm run dev`).
2. In `react-supabase-auth-template`, set `VITE_API_BASE_URL=http://localhost:8787` in `.env.local`.
3. Start the frontend (`bun run dev`).
4. Sign in with Google OAuth or email/password; the home page calls `GET /me` and the header polls `GET /health`.
5. Call `POST /chat` from your frontend with the same Bearer token to add an AI prompt UI (see [`index.md`](index.md)).

## 6. Deploy

See [`CLOUDFLARE_SETUP.md`](CLOUDFLARE_SETUP.md) for `wrangler deploy`, production secrets, and `wrangler secret put GEMINI_API_KEY`.
