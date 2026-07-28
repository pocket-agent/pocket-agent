# Pocket Agent Development Instructions


You are developing Pocket Agent.

Pocket Agent is a private personal AI assistant running on user-owned infrastructure.


# Primary Objective

Create a reliable 24/7 AI assistant capable of interacting with personal files and performing useful workflows safely.


# Important Rules


## Never Allow Direct LLM File Modification

The LLM reasons.

The tools execute.


Wrong:

```
LLM edits spreadsheet
```


Correct:

```
LLM

↓

update_excel_tool()

↓

openpyxl

↓

validated file

```


# File Safety Rules


Never modify original files immediately.


Required workflow:

```
Original File

↓

Backup

↓

Working Copy

↓

Modification

↓

Validation

↓

Replace

```


Every operation must create logs.


# Supported File Libraries


PDF:

```
PyMuPDF
pdfplumber
```


Excel:

```
openpyxl
pandas
```


Documents:

```
python-docx
```


# Code Standards


Use:

- Python 3.12+
- Type hints
- Async where useful
- Small modules
- Clear naming


Avoid:

- Giant files
- Hidden behavior
- Hardcoded secrets


# LLM Rules


Never hardcode one provider.


Support:

- Gemini
- Claude
- OpenAI
- Ollama


Use an abstraction layer.


# Skills


Every capability should be a skill.


A skill defines:

- Purpose
- Tools
- Instructions
- Examples
- Limitations


# Development Priority


1. Telegram communication
2. File indexing
3. NAS integration
4. Document reading
5. Safe editing
6. Memory
7. Dashboard


# Cursor Instructions


Before implementing:

1. Read all documentation.
2. Understand architecture.
3. Create a plan.
4. Implement minimally.
5. Add tests.
6. Update documentation.


Never create features that violate architecture.


# OKF specs and agent skills

| Resource | Path |
|----------|------|
| Feature contracts | [specs/features/](specs/features/) |
| OKF bundle root | [index.md](index.md) |
| Developer skill catalog | [.agents/skills/README.md](.agents/skills/README.md) |
| Cursor packs | `.agents/skills/pocket-agent/SKILL.md` (start here) |

Runtime skills (loaded by the agent) live in `agent/skills/`. Developer guides live in `.agents/skills/`.