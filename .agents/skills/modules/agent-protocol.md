# Agent protocol module

Recreate agent behavior constraints when implementing planner, router, or response formatting.

## Reasoning loop

1. Understand request
2. Identify skill
3. Select tools
4. Execute safely
5. Validate result
6. Explain outcome

## Hard stops

- Do not guess file paths — use `search_files` or configured roots
- Do not delete without explicit user approval
- Do not modify without backup workflow
- Do not expose secrets in responses or memory

## Memory rules

Store preferences and long-term non-sensitive facts. Never store passwords, tokens, or API keys.

## Human approval gates

Require confirmation before: deletion, large modifications, external sharing, irreversible operations.

## Communication

Responses: concise, clear, action oriented.

## References

- [AGENT_PROTOCOL.md](../../../AGENT_PROTOCOL.md)
- [specs/features/03-agent-protocol.md](../../../specs/features/03-agent-protocol.md)
