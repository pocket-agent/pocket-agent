---
type: Playbook
title: Gemini client
description: Server-side @google/genai chat completion with history.
tags: [gemini, ai]
timestamp: 2026-07-15T00:00:00Z
resource: src/lib/gemini.ts
---

# Config

* `GEMINI_API_KEY` from worker secrets (`.dev.vars` locally)
* Optional `GEMINI_MODEL` (default `gemini-2.5-flash`)

# Pattern

Build multi-turn contents from `history` + latest `message`, call Gemini generate, return text reply.

Never log or return the API key.

See [specs/features/08-gemini-integration.md](../../specs/features/08-gemini-integration.md).
