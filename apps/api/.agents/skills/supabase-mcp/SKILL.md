---
name: supabase-mcp
description: Apply Supabase migrations, seed data, and inspect schema using Supabase MCP from cf-hono-supabase-gemini-api-template work. Use when creating tables, running SQL, checking RLS advisors, or seeding dev data for new API endpoints.
---

# Supabase MCP (Database)

Use when new API endpoints need **Postgres tables**, not for the default `/health` + `/me` template (auth-only).

## Prerequisites

- Supabase MCP server enabled in Cursor (plugin-supabase or user-supabase)
- Project linked to the same Supabase instance as worker env vars

**Before schema changes:** read MCP tool schemas, then `list_tables` to see current structure.

## Workflow

### 1. Inspect existing schema

```
list_tables → understand current public schema
get_advisors → security/performance recommendations after changes
```

### 2. Create migration

Prefer MCP `apply_migration` with a descriptive name:

```
name: create_widgets_table
query: |
  CREATE TABLE public.widgets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
  );

  ALTER TABLE public.widgets ENABLE ROW LEVEL SECURITY;

  CREATE POLICY "Users read own widgets"
    ON public.widgets FOR SELECT
    USING (auth.uid() = user_id);

  CREATE POLICY "Users insert own widgets"
    ON public.widgets FOR INSERT
    WITH CHECK (auth.uid() = user_id);
```

### 3. Verify

- `list_tables` — table exists
- `get_advisors` — no missing RLS warnings
- Test via worker route using `getSupabaseClientWithJWT`

### 4. Seed dev data (optional)

Use `execute_sql` for idempotent seeds in dev only:

```sql
INSERT INTO public.widgets (user_id, name)
SELECT id, 'Demo widget'
FROM auth.users
LIMIT 1
ON CONFLICT DO NOTHING;
```

Never seed service role keys or production PII.

## RLS checklist

- [ ] `ENABLE ROW LEVEL SECURITY` on every public table exposed to API
- [ ] SELECT policy for reads
- [ ] INSERT policy with `WITH CHECK (auth.uid() = user_id)` for user-owned rows
- [ ] UPDATE needs SELECT policy too (Postgres RLS quirk)
- [ ] Avoid `user_metadata` in policies — use `auth.uid()` or `app_metadata`

## Local CLI alternative

If MCP unavailable and shell access exists:

```bash
supabase migration new create_widgets_table
# edit supabase/migrations/<timestamp>_create_widgets_table.sql
supabase db push
```

Discover commands via `supabase --help`; do not guess flags.

## Wire to worker

1. Zod schema → [create-zod-schema](../create-zod-schema/SKILL.md)
2. Route using JWT client → [create-api-endpoint](../create-api-endpoint/SKILL.md)
3. Document table + policies in `index.md`

## Data API exposure

New tables may need `GRANT` to `authenticated` / `anon` depending on project Data API settings. RLS still required.

## See also

- Upstream Supabase skill (if bundled): `.agents/skills/supabase/SKILL.md` in frontend repo
- [authentication](../authentication/SKILL.md)
