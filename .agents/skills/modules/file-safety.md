# File safety module

Recreate safe file workflows for any tool that touches user documents.

## Mandatory pipeline

```
Original File
    ↓
Backup (data/backup/ or NAS backup path with timestamp)
    ↓
Working Copy (data/working/)
    ↓
Modification (tool execution)
    ↓
Validation (structure, checksum, size bounds)
    ↓
Replace original (only after validation passes)
```

## Never

- Modify the original file in place as the first step
- Skip logging
- Skip validation before replace

## Permissions

| Operation | Default |
|-----------|---------|
| Read | Required documents only |
| Write | Working directory and controlled replace |
| Delete | Never without explicit user confirmation |

## Logging fields

- Timestamp
- User request (or request id)
- Tool name
- Source path
- Backup path
- Result (success/failure)
- Error detail if failed

## References

- [SECURITY.md](../../../SECURITY.md)
- [INSTRUCTIONS.md](../../../INSTRUCTIONS.md) — File Safety Rules
- [specs/features/06-security.md](../../../specs/features/06-security.md)
