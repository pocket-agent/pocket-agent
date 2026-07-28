---
name: create-api-endpoint
description: Add REST endpoints to cf-hono-supabase-gemini-api-template Hono worker. Use when creating routes, registering routers in index.ts, choosing public vs JWT-protected handlers, or returning standardized JSON responses.
---

# Create API Endpoints

## Before you start

Read [`index.md`](../../index.md). Existing endpoints: `GET /health`, `GET /me`, `POST /chat`, `GET /chat`.

## Response shape

Always use helpers from `src/utils/response.ts`:

```typescript
import { successResponse, errorResponse } from "@/utils/response";

return c.json(successResponse({ id: "..." }));
return c.json(errorResponse("Not found", "NOT_FOUND"), { status: 404 });
```

## Public endpoint (no JWT)

1. Create `src/routes/<name>.ts` with a Hono sub-router
2. Register in `src/index.ts` **before** `app.use("/*", authMiddleware)`

Example — `health.ts`:

```typescript
export const healthRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

healthRouter.get("/", async (c) => {
  return c.json(successResponse({ status: "healthy", timestamp: new Date().toISOString() }));
});
```

```typescript
// index.ts
app.route("/health", healthRouter);
app.use("/*", authMiddleware);
```

Mounted at `/health` → `GET /health`.

## Protected endpoint (JWT required)

1. Create router in `src/routes/`
2. Register **after** `authMiddleware` in `index.ts`
3. Read `c.get("userId")` if set by middleware (or re-extract token for Supabase calls)

Example — `me.ts` pattern:

```typescript
import { getSupabaseClientWithJWT } from "@/lib/supabase";
import { extractJWT } from "@/utils/jwt";

meRouter.get("/", async (c) => {
  const token = extractJWT(c.req.header("Authorization") || null);
  if (!token) {
    return c.json(errorResponse("Unauthorized", "UNAUTHORIZED"), { status: 401 });
  }
  const supabase = getSupabaseClientWithJWT(c.env, token);
  const { data, error } = await supabase.auth.getUser();
  // ...
});
```

## Registering a new resource

```typescript
// src/routes/widgets.ts
export const widgetsRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

widgetsRouter.get("/", async (c) => {
  const userId = c.get("userId");
  // ...
  return c.json(successResponse(items));
});

// src/index.ts
app.use("/*", authMiddleware);
app.route("/me", meRouter);
app.route("/widgets", widgetsRouter);
```

## Validation

For POST/PUT/PATCH bodies, validate with Zod — see [create-zod-schema](../create-zod-schema/SKILL.md).

```typescript
import { zValidator } from "@hono/zod-validator";
import { createWidgetSchema } from "@/schemas/widget.schema";

widgetsRouter.post("/", zValidator("json", createWidgetSchema), async (c) => {
  const input = c.req.valid("json");
  // ...
});
```

## Supabase data access

| Need | Client |
|------|--------|
| User-scoped rows (RLS) | `getSupabaseClientWithJWT(env, token)` |
| No user context | `getSupabaseUserClient(env)` |
| Admin bypass (rare) | `getSupabaseAdminClient(env)` |

Prefer JWT-scoped client for user data. See [authentication](../authentication/SKILL.md).

## Checklist

- [ ] Route file under `src/routes/`
- [ ] Registered in `index.ts` at correct middleware position
- [ ] Uses `successResponse` / `errorResponse`
- [ ] Documented in `index.md`
- [ ] Frontend module added in react template `src/api/` if consumed by UI
- [ ] `npm run type-check` passes

## See also

- [`index.md`](../../../index.md) — OKF feature index
- [chat-route](../modules/chat-route.md) — OKF module for `/chat` (when adding chat endpoints)
- [authentication](../authentication/SKILL.md)
- [supabase-mcp](../supabase-mcp/SKILL.md) — when endpoint needs new tables
