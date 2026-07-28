# Pocket Agent Security


Pocket Agent manages private information.

Security is a core requirement.


# Secrets


Never store:

- API keys
- Tokens
- Passwords

inside git.


Use:

```
.env
```


# File Permissions


Default:

Read:

Required documents


Write:

Working directory only


Delete:

Never without confirmation


# Backups


Before modification:

```
document.xlsx

↓

backup/document_timestamp.xlsx

```


# Logging


Every action must record:


- Timestamp
- User request
- Tool used
- Result
- Errors


# Network


External communication must be authenticated.


Allowed:

- Telegram API
- LLM APIs


Avoid exposing local services publicly.


# Principle


The agent should be powerful but not destructive.