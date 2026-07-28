# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-08

### Added

- **Cloudflare Worker** API built with **Hono** and TypeScript (`wrangler dev` / `wrangler deploy`).
- **`GET /health`** — public liveness endpoint for frontend connectivity checks.
- **`GET /me`** — authenticated profile endpoint using `Authorization: Bearer <supabase_access_token>` and `auth.getUser()`.
- **`POST /chat`** — Bearer-protected chat completion with `{ "message": "..." }` and optional `history` for multi-turn context.
- **`GET /chat?message=`** — query-string alternative for quick manual tests (no history).
- **JWT auth middleware** — validates Supabase access tokens on all routes except `/health`.
- **AI provider integration** — `@google/genai` with `GEMINI_API_KEY` and optional `GEMINI_MODEL` (default `gemini-2.5-flash`).
- **Standardized JSON responses** — `{ success, data }` / `{ success: false, error }` via `src/utils/response.ts`.
- **CORS** — configurable via `ALLOWED_ORIGINS` for local dev and production frontends.
- **Supabase client helpers** — JWT-scoped, anonymous, and service-role clients in `src/lib/supabase.ts`.
- **Request logging** and centralized error handling middleware.
- **Feature specification** at [`index.md`](index.md).
- **Pairing** with [react-supabase-auth-ai-chat-template](https://github.com/open-templates/react-supabase-auth-ai-chat-template) for end-to-end auth + chat demo.
- **Template init wizard** and shared `@open-templates/specs` scaffolding.

---

## Repository documents

[README](README.md) | [INSTRUCTIONS](INSTRUCTIONS.md) | **CHANGELOG** | [CONTRIBUTING](CONTRIBUTING.md) | [SECURITY](SECURITY.md) | [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)
