---
name: authentication
description: JWT authentication and Supabase client usage in cf-hono-supabase-gemini-api-template. Use when securing routes, implementing /me-style handlers, choosing anon vs JWT vs service-role clients, or debugging 401 responses.
---

# Authentication

## Model

1. User signs in via **Supabase Auth** in the React app
2. Browser sends `Authorization: Bearer <access_token>` to the worker
3. `authMiddleware` validates JWT and sets `userId` (`sub` claim)
4. Handlers use Supabase clients scoped to that user when touching Postgres

## Middleware (`src/middleware/index.ts`)

```typescript
app.route("/health", healthRouter);  // public — no auth
app.use("/*", authMiddleware);       // everything below requires valid JWT
app.route("/me", meRouter);
```

`authMiddleware` calls `getAuthenticatedUser()` → `verifyJWT()` → sets `c.set("userId", userId)`.

## JWT utilities (`src/utils/jwt.ts`)

- `extractJWT(authHeader)` — parse `Bearer <token>`
- `verifyJWT(token, env)` — decode/validate payload; requires `sub`

For production hardening, verify signature against Supabase JWKS (see Supabase docs). Current template checks payload structure.

## Supabase clients (`src/lib/supabase.ts`)

| Function | Key | Use |
|----------|-----|-----|
| `getSupabaseClientWithJWT(env, token)` | anon + Bearer | **Default for user data** — respects RLS |
| `getSupabaseUserClient(env)` | anon | Unauthenticated public reads |
| `getSupabaseAdminClient(env)` | service_role | Admin-only; never expose to browser |

### `/me` pattern (auth only, no custom tables)

```typescript
const supabase = getSupabaseClientWithJWT(c.env, token);
const { data, error } = await supabase.auth.getUser();
```

Returns the user associated with the JWT without service role.

### User-owned rows (after migrations)

```typescript
const token = extractJWT(c.req.header("Authorization") || null)!;
const supabase = getSupabaseClientWithJWT(c.env, token);
const { data, error } = await supabase.from("widgets").select("*");
// RLS policies filter by auth.uid()
```

## Public routes

Only mount **before** `authMiddleware`. Do not skip auth inside a protected router.

## CORS + credentials

`ALLOWED_ORIGINS` env (comma-separated) restricts browser origins. Frontend must send `Authorization` header; `apiFetch` handles this.

## Error responses

```typescript
return c.json(errorResponse("Unauthorized", "UNAUTHORIZED"), { status: 401 });
```

## Security rules

- Never log full JWTs
- Never return `SUPABASE_SERVICE_ROLE_KEY` in responses
- Do not use `user_metadata` for authorization decisions (user-editable)
- Prefer RLS + JWT client over service role for user CRUD

## Frontend token flow

React app stores token in `localStorage['x-auth-token']`. On 401, client refreshes session and retries once.

## See also

- [`index.md`](../../../index.md) — OKF feature index
- [auth-middleware](../modules/auth-middleware.md) — OKF module for JWT gate
- [chat-route](../modules/chat-route.md) — OKF module for `/chat`
- [create-api-endpoint](../create-api-endpoint/SKILL.md)
