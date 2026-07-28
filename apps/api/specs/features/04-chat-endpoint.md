---
type: API Endpoint
title: POST /chat
description: Multi-turn Gemini completion with optional conversation history.
tags: [api, chat, gemini]
timestamp: 2026-07-15T00:00:00Z
resource: POST /chat
---

# `POST /chat`

* **Authentication:** Bearer JWT
* **Body:**

```json
{
  "message": "Follow-up question",
  "history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ]
}
```

* `history` optional; up to **100** prior turns
* **Success:**

```json
{
  "success": true,
  "data": {
    "message": "...",
    "reply": "...",
    "model": "gemini-2.5-flash"
  }
}
```

* **Errors:** `400`, `401`, `502` (Gemini failure)

# `GET /chat?message=...`

Same auth and response shape for quick manual tests.

See [.agents/skills/modules/chat-route.md](../../.agents/skills/modules/chat-route.md).
