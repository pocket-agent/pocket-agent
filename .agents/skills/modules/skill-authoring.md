# Skill authoring module

Recreate runtime skills when adding domain knowledge to `agent/skills/`.

## File format

One markdown file per domain, e.g. `agent/skills/pdf.md`.

Required sections:

```markdown
# PDF

## Purpose
What problem this skill solves.

## Tools
- extract_pdf_text
- modify_pdf

## Instructions
How the agent should behave for PDF tasks.

## Examples
- "Summarize this tax PDF"
- "Extract tables from invoice.pdf"

## Limitations
- Do not modify without backup
- Do not guess file paths
```

## Rules

- Small and focused — split large domains into multiple skills
- Reference tools by name; implementation stays in `agent/tools/`
- Align limitations with [AGENT_PROTOCOL.md](../../../AGENT_PROTOCOL.md)

## Distinction

| Path | Audience |
|------|----------|
| `agent/skills/*.md` | Pocket Agent runtime |
| `.agents/skills/` | Developers and Cursor |

## References

- [SKILLS.md](../../../SKILLS.md)
- [specs/features/05-skill-system.md](../../../specs/features/05-skill-system.md)
