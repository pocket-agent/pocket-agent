---
type: Feature
title: Security
description: Secrets, file permissions, backups, logging, and network boundaries.
tags: [security]
timestamp: 2026-07-28T00:00:00Z
---

Pocket Agent manages private information. Security is a core requirement. Canonical reference: [SECURITY.md](../../SECURITY.md).

## Secrets

Never commit API keys, tokens, or passwords. Use `.env` locally.

## File permissions

| Operation | Default |
|-----------|---------|
| Read | Required documents only |
| Write | Working directory only |
| Delete | Never without explicit confirmation |

## Backup workflow

Before any modification:

```
document.xlsx → backup/document_timestamp.xlsx → working copy → modify → validate → replace
```

## Logging

Every action records: timestamp, user request, tool used, result, errors.

## Network

Authenticated external communication only. Allowed: Telegram API, LLM APIs. Do not expose local services publicly.

## Principle

The agent should be powerful but not destructive.
