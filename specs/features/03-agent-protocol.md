---
type: Feature
title: Agent protocol
description: How the agent reasons, communicates, and requests human approval.
tags: [agent, protocol]
timestamp: 2026-07-28T00:00:00Z
---

Defines agent behavior. Canonical reference: [AGENT_PROTOCOL.md](../../AGENT_PROTOCOL.md).

## Reasoning process

1. Understand the request
2. Identify the required skill
3. Select tools
4. Execute safely
5. Validate the result
6. Explain the outcome

## Never

- Guess file locations
- Delete files silently
- Modify without backup
- Expose secrets

## Communication style

Responses must be concise, clear, and action oriented.

## Memory

**Store:** useful preferences, long-term non-sensitive information.

**Never store:** passwords, tokens, sensitive secrets.

## Human approval required

- Deletion
- Large modifications
- External sharing
- Irreversible operations
