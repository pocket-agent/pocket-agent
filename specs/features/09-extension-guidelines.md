---
type: Playbook
title: Extension guidelines
description: How to add tools, skills, specs, and agent guides without violating architecture.
tags: [extension]
timestamp: 2026-07-28T00:00:00Z
---

## Adding a tool

1. Implement in `agent/tools/` with validation, logging, and error handling
2. Document in [TOOLS_SPEC.md](../../TOOLS_SPEC.md)
3. Add tests under `tests/`
4. Reference from relevant `agent/skills/*.md` modules
5. If user-visible behavior changes, update `specs/features/04-tool-system.md`

## Adding a runtime skill

1. Create `agent/skills/<name>.md` following [SKILLS.md](../../SKILLS.md) structure
2. List tools, instructions, examples, and limitations
3. Register with the skill loader when that component exists

## Adding developer guides

1. Add recreation guide in `.agents/skills/modules/` for non-obvious patterns
2. Add Cursor `SKILL.md` pack under `.agents/skills/<pack>/` when procedural automation helps
3. List new guides in [.agents/skills/README.md](../../.agents/skills/README.md)

## Adding feature specs

1. Document user-visible behavior in `specs/features/`
2. Link from root [index.md](../../index.md)
3. Log structural changes in [specs/log.md](../log.md)

## Architecture violations (reject in review)

- LLM directly reading/writing files without tools
- Modifying originals without backup
- Hardcoded API keys or single LLM provider
- Deletion or external sharing without human approval

## Every feature must include

- Documentation
- Tests
- Error handling
- Security consideration
