---
type: Playbook
title: Extension guidelines
description: Add routes, document in OKF specs, keep response shape consistent.
tags: [extension]
timestamp: 2026-07-15T00:00:00Z
---

1. Register routers after `authMiddleware` unless public.
2. Prefer JWT-scoped Supabase clients for user data.
3. Use `src/utils/response.ts` JSON shape.
4. Add `specs/features/` concepts and `.agents/skills/modules/` guides.
5. Update frontend `specs/` and `src/api/` in the paired repo.
