---
name: safe-file-ops
description: >-
  Implement safe file read/write/edit in Pocket Agent. Use when modifying PDFs,
  Excel, Word, NAS files, backups, validation, or any tool that touches user
  documents.
---

# Safe file operations

All file modifications in Pocket Agent follow a strict pipeline.

## Pipeline

```
Original → Backup (timestamped) → Working copy → Tool execution → Validation → Replace
```

## Never

- Modify the original file as the first step
- Skip backup or validation
- Write outside `data/working/` or configured safe paths without explicit design
- Delete without explicit user confirmation

## Backup path pattern

```
backup/document_YYYYMMDD_HHMMSS.xlsx
```

## Logging (required)

Record: timestamp, user request, tool name, paths, result, errors.

## Libraries

| Type | Libraries |
|------|-----------|
| PDF | PyMuPDF, pdfplumber |
| Excel | openpyxl, pandas |
| Word | python-docx |

## References

- [SECURITY.md](../../SECURITY.md)
- [INSTRUCTIONS.md](../../INSTRUCTIONS.md)
- [modules/file-safety.md](../modules/file-safety.md)
- [specs/features/06-security.md](../../specs/features/06-security.md)
