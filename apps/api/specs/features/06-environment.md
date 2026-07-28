---
type: Reference
title: Environment
description: Required Gemini secrets and optional model override.
tags: [config, gemini]
timestamp: 2026-07-15T00:00:00Z
---

| Variable | Required | Purpose |
|----------|----------|---------|
| `GEMINI_API_KEY` | Yes | Google AI Studio key for `@google/genai` |
| `GEMINI_MODEL` | No | Default `gemini-2.5-flash` |

Local dev: `.dev.vars`. Never commit secrets.
