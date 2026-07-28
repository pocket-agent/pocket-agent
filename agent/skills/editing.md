# Safe editing

Controlled file modifications with backup, validation, and replace.

## Purpose

Edit Excel, Word, and PDF files without destroying originals.

## Tools

- modify_excel
- modify_docx
- modify_pdf

## Instructions

Every edit follows: backup → working copy → modify → validate → replace.
Always report backup path to the user.
Single-cell or single-paragraph edits only via Telegram commands.
Require explicit user intent — never batch-edit without approval.

## Examples

- "/edit_excel budget.xlsx Budget B2=2500"
- "/edit_word notes.docx append Meeting notes for today"
- "/edit_pdf report.pdf add_page Appendix A"

## Limitations

- No deletion
- No multi-file edits in one command
- No edits outside allowed NAS roots
- Files over 50MB are rejected
