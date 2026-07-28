## Telegram commands

| Command | Action |
|---------|--------|
| `/start` | Welcome message |
| `/help` | Command list |
| `/index` | Rebuild SQLite file index on NAS |
| `/nas` | List files at NAS root |
| `/search <query>` | Search indexed files (name/path) |
| `/read <path>` | Read TXT, DOCX, PDF, or XLSX summary |
| `/pdf <path>` | Extract PDF text |
| `/excel <path>` | Analyze Excel workbook structure |
| `/edit_excel <path> <sheet> <cell>=<value>` | Safe single-cell Excel edit |
| `/edit_word <path> append\|replace_last <text>` | Safe Word paragraph edit |
| `/edit_pdf <path> add_page <text>` | Add PDF page with text |
| `/remember <text>` | Store personal memory (no secrets) |
| `/recall <query>` | Search your memories |
| `/kb <query>` | Search knowledge base |
| `/kb_index` | Index NAS text/PDF into knowledge base |
| Any text | LLM with memory + skill context (Gemini when configured) |

## Testing

```bash
pytest
ruff check src tests
```

## Architecture reference

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [INSTRUCTIONS.md](INSTRUCTIONS.md)
- [specs/features/](specs/features/)

## Status

**Phase 1** — Foundation: Python package, Telegram bot, Gemini, config, NAS access.

**Phase 2** — File intelligence: SQLite index, indexed search, PDF extraction, DOCX/TXT read, Excel analysis.

**Phase 3** — Safe editing: backup/working/validate/replace pipeline for Excel, Word, and PDF.

**Phase 4** — Memory: personal memories, FTS + Gemini vector search, knowledge base, skill retrieval in prompts.

Next (Phase 5): React dashboard on Cloudflare Pages.
