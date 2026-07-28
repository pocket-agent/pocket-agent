---
type: Feature
title: Tool system
description: Deterministic functions the runtime executes; LLM selects, never performs file ops.
tags: [tools]
timestamp: 2026-07-28T00:00:00Z
---

The LLM selects tools. The runtime executes them. Canonical reference: [TOOLS_SPEC.md](../../TOOLS_SPEC.md).

## Principles

- Tools are deterministic Python functions
- Every tool validates inputs, handles errors, produces logs, and has documentation
- The LLM never directly manipulates files

## File tools

| Tool | Purpose |
|------|---------|
| `search_files()` | Search NAS files by query, location, filters |
| `read_file()` | Read PDF, TXT, DOCX, XLSX |

## Excel tools

| Tool | Purpose |
|------|---------|
| `analyze_excel()` | Read workbook structure |
| `modify_excel()` | Apply controlled changes (backup + validate required) |

## PDF tools

| Tool | Purpose |
|------|---------|
| `extract_pdf_text()` | Extract text from PDFs |
| `modify_pdf()` | Controlled PDF modifications |

## Communication tools

| Tool | Purpose |
|------|---------|
| `send_telegram()` | Send response to user |

## Supported libraries

- PDF: PyMuPDF, pdfplumber
- Excel: openpyxl, pandas
- Documents: python-docx

## Adding a tool

1. Implement under `agent/tools/`
2. Document in [TOOLS_SPEC.md](../../TOOLS_SPEC.md)
3. Wire into skill modules that need it
4. Add tests and logging
