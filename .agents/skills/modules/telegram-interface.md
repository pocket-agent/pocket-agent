# Telegram interface module

Recreate the interface layer when implementing or extending the Telegram bot.

## Responsibilities

- Receive user messages and commands
- Authenticate allowed users (Telegram user id allowlist)
- Forward normalized requests to agent core
- Return formatted responses via `send_telegram` tool or interface adapter
- Support notifications and scheduled messages (future)

## Flow

```
Telegram message → Interface adapter → Agent core → ... → send_telegram → User
```

## Security

- Validate Telegram webhook/token via `.env`
- Do not expose local agent HTTP without authentication
- Log inbound commands with user id (not message secrets)

## Phase 1 priority

Telegram is the first interface per [ROADMAP.md](../../../ROADMAP.md). Implement before dashboard.

## References

- [ARCHITECTURE.md](../../../ARCHITECTURE.md) — Interface Layer
- [TOOLS_SPEC.md](../../../TOOLS_SPEC.md) — `send_telegram()`
- [specs/features/08-roadmap.md](../../../specs/features/08-roadmap.md)
