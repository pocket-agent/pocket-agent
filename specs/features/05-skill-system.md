---
type: Feature
title: Skill system
description: Reusable knowledge modules loaded dynamically by the agent core.
tags: [skills]
timestamp: 2026-07-28T00:00:00Z
---

Skills are runtime knowledge modules in `agent/skills/`. Canonical reference: [SKILLS.md](../../SKILLS.md).

## Skill structure

Each skill defines:

| Section | Content |
|---------|---------|
| Purpose | Problem it solves |
| Tools | Callable tools |
| Instructions | Agent behavior for this domain |
| Examples | Typical user requests |
| Limitations | What the skill must not do |

## Example skills (planned)

```
agent/skills/pdf.md
agent/skills/excel.md
agent/skills/finance.md
agent/skills/travel.md
agent/skills/contracts.md
```

## Design rules

- Small and focused — one domain per file
- Skills reference tools, not implement them
- Align with [AGENT_PROTOCOL.md](../../AGENT_PROTOCOL.md) safety rules

## Distinction: runtime skills vs Cursor skills

| Location | Purpose |
|----------|---------|
| `agent/skills/*.md` | Loaded by Pocket Agent at runtime for task routing |
| `.agents/skills/` | OKF guides and Cursor `SKILL.md` packs for developers |
