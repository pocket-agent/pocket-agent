---
type: Feature
title: HTTP API
description: FastAPI app served by pocket-agent serve on port 8787.
tags: [http, api, fastapi]
timestamp: 2026-08-20T00:00:00Z
---

# HTTP API

Default bind: `127.0.0.1:8787` (see `config/settings.yaml`).

| Route | Method | Description |
|-------|--------|-------------|
| `/health` | GET | Liveness |
| `/status` | GET | Agent status payload |
| `/me` | GET | Profile (auth-aware) |
| `/chat` | POST | Chat completion via Pocket Node |
| `/settings/*` | GET/PATCH | User settings |

When `http.serve_static` is enabled, built UI from `pocket-agent-app/dist/client` may be served for bundled/desktop flows.

Response envelopes should match `pocket-agent-sdk` schemas. Update SDK when shapes change.
