---
type: Playbook
title: Chat route
description: Validate body, cap history, call Gemini, return reply JSON.
tags: [chat, api, gemini]
timestamp: 2026-07-15T00:00:00Z
resource: src/routes/chat.ts
---

1. Parse `{ message, history }` from JSON body (or `message` query param for GET)
2. Validate non-empty `message`
3. Trim `history` to max **100** turns
4. Call `generateChatReply` from `src/lib/gemini.ts`
5. Return `{ success: true, data: { message, reply, model } }`

See [specs/features/04-chat-endpoint.md](../../specs/features/04-chat-endpoint.md).
