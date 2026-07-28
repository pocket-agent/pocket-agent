---
type: Feature
title: Frontend pairing
description: Contract with Supabase auth AI chat SPAs.
tags: [pairing, frontend]
timestamp: 2026-07-16T00:00:00Z
---

| Frontend call | Backend route |
|---------------|---------------|
| Health indicator | `GET /health` |
| Home profile | `GET /me` |
| AI chat | `POST /chat` with `{ message, history }` |

Base URL in frontends: `VITE_API_BASE_URL` (default `http://localhost:8787`).

## Paired frontend templates (same contract)

| Template | Stack |
|----------|-------|
| [react-supabase-auth-ai-chat-template](https://github.com/open-templates/react-supabase-auth-ai-chat-template) | React |
| [vue-supabase-auth-ai-chat-template](https://github.com/open-templates/vue-supabase-auth-ai-chat-template) | Vue |
| [svelte-supabase-auth-ai-chat-template](https://github.com/open-templates/svelte-supabase-auth-ai-chat-template) | Svelte |
| [astro-supabase-auth-ai-chat-template](https://github.com/open-templates/astro-supabase-auth-ai-chat-template) | Astro |
