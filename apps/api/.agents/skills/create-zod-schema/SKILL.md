---
name: create-zod-schema
description: Define Zod validation schemas for cf-hono-supabase-gemini-api-template request and response bodies. Use when adding POST/PUT/PATCH endpoints, validating query params, or typing API inputs before Supabase operations.
---

# Create Zod Schemas

## When to use

- **Request bodies** — POST/PUT/PATCH with `@hono/zod-validator`
- **Shared types** — infer TypeScript types from schemas
- **Not required** — simple GET handlers with no input (e.g. `/health`, `/me`)

## File location

`src/schemas/<resource>.schema.ts`

The default template has no schemas until you add domain tables. Create the `schemas/` file alongside the route.

## Pattern

```typescript
import { z } from "zod";

export const createWidgetSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().optional(),
});

export const updateWidgetSchema = createWidgetSchema.partial();

export type CreateWidgetInput = z.infer<typeof createWidgetSchema>;
export type UpdateWidgetInput = z.infer<typeof updateWidgetSchema>;
```

## Wire to Hono route

```typescript
import { zValidator } from "@hono/zod-validator";
import { createWidgetSchema } from "@/schemas/widget.schema";

widgetsRouter.post(
  "/",
  zValidator("json", createWidgetSchema),
  async (c) => {
    const input = c.req.valid("json");
    // input is typed
  }
);
```

## Query params

```typescript
const listQuerySchema = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(20),
  offset: z.coerce.number().int().min(0).default(0),
});

widgetsRouter.get("/", zValidator("query", listQuerySchema), async (c) => {
  const { limit, offset } = c.req.valid("query");
});
```

## Response documentation

Zod schemas validate **incoming** data. Outgoing responses use `successResponse()`; optionally define a Zod schema for documentation/tests:

```typescript
export const widgetResponseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  user_id: z.string().uuid(),
  created_at: z.string(),
});
```

## Conventions

- `create*Schema` — required fields for insert
- `update*Schema` — `.partial()` of create schema
- Use `z.coerce` for query string numbers
- UUID fields: `z.string().uuid()`
- Enums: `z.enum(["draft", "published"])`

## After schema + table exist

1. Apply migration via [supabase-mcp](../supabase-mcp/SKILL.md)
2. Enable RLS on new tables
3. Use `getSupabaseClientWithJWT` in the route handler
4. Update `index.md`

## See also

- [create-api-endpoint](../create-api-endpoint/SKILL.md)
