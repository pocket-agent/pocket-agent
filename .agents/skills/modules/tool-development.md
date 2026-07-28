# Tool development module

Recreate tools when adding capabilities under `agent/tools/`.

## Contract

Every tool is a deterministic function:

- Validates inputs before execution
- Handles errors without silent failure
- Writes structured logs (timestamp, tool name, inputs summary, result/errors)
- Has documentation in [TOOLS_SPEC.md](../../../TOOLS_SPEC.md)

## Implementation checklist

1. Create module in `agent/tools/<category>/`
2. Define typed inputs/outputs (Python 3.12+ type hints)
3. Use async only when I/O-bound (NAS, network, LLM)
4. Never read/write user files outside approved paths
5. For edits: delegate to file-safety workflow (backup → working copy)
6. Register tool for agent core tool registry
7. Add tests in `tests/tools/`

## Libraries by domain

| Domain | Libraries |
|--------|-------------|
| PDF | PyMuPDF, pdfplumber |
| Excel | openpyxl, pandas |
| Documents | python-docx |

## References

- [TOOLS_SPEC.md](../../../TOOLS_SPEC.md)
- [specs/features/04-tool-system.md](../../../specs/features/04-tool-system.md)
- [file-safety](file-safety.md)
