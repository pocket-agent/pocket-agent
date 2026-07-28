---
name: add-runtime-skill
description: >-
  Add a Pocket Agent runtime skill in agent/skills/. Use when creating domain
  knowledge for PDF, Excel, finance, contracts, travel, or other agent domains.
---

# Add a runtime skill

Runtime skills live in `agent/skills/*.md` and are loaded by the agent core skill loader.

## File structure

```markdown
# Skill Name

## Purpose
What problem this skill solves.

## Tools
- tool_name_one
- tool_name_two

## Instructions
How the agent should behave in this domain.

## Examples
- Typical user request 1
- Typical user request 2

## Limitations
- What this skill must not do
```

## Rules

- One domain per file; keep skills small
- List tools by name — implementation stays in `agent/tools/`
- Limitations must align with [AGENT_PROTOCOL.md](../../AGENT_PROTOCOL.md)
- Do not duplicate tool implementation in the skill file

## Distinction

| Location | Purpose |
|----------|---------|
| `agent/skills/*.md` | Runtime — loaded by Pocket Agent |
| `.agents/skills/` | Development guides for Cursor |

## References

- [SKILLS.md](../../SKILLS.md)
- [modules/skill-authoring.md](../modules/skill-authoring.md)
- [specs/features/05-skill-system.md](../../specs/features/05-skill-system.md)
