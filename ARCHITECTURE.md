# Pocket Agent Architecture


# Overview

Pocket Agent is a personal AI system with six internal layers plus a **client/API edge** (web, worker, desktop, CLI) that routes user actions to a **Pocket Node** Python agent. External LLM APIs are never called from the browser.

Hosted and local clients never call external LLM APIs directly. They authenticate with **Google OAuth** (single Google Cloud client ID shared by web and Tauri) and send actions to the **API worker**, which proxies to the **Pocket Node** Python agent.

| Component | Path | Deploy |
|-----------|------|--------|
| Web UI | `apps/web` | Cloudflare Pages |
| API gateway | `apps/api` | Cloudflare Worker |
| Desktop | `apps/desktop` | Tauri install |
| CLI | `apps/cli` | Desktop install (future) |
| Agent | `src/pocket_agent` | Pocket Node (`pocket-agent serve`) |

```
Browser / Tauri  →  Google OAuth (client ID in app)
       ↓
  apps/api (Worker)  →  verifies Google token
       ↓
  Pocket Node agent  →  LLM keys, tools, NAS, memory
       ↑
  cloudflared tunnel (production, optional)
```

See [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md). Clone app repos: `pocket-agent init`.


## Internal layers


## Interface Layer

Responsible for user communication.


Current:

- Telegram


Planned (monorepo):

- Web dashboard — `apps/web` (React, Cloudflare Pages, Google OAuth)
- API gateway — `apps/api` (Cloudflare Worker → Pocket Node)
- Desktop app — `apps/desktop` (Tauri, same Google OAuth client as web)


Future:

- Mobile clients (optional)


Responsibilities:

- Receive requests
- Authenticate users
- Return responses


---


## Agent Core


Responsible for reasoning.


Components:

- Router
- Planner
- Memory Manager
- Skill Loader


Responsibilities:

- Understand requests
- Select actions
- Manage workflows


---


## Tool Layer


Responsible for execution.


Examples:

```
search_files

read_document

modify_excel

generate_pdf

send_message

```


Tools are deterministic.


---


## Storage Layer


Storage sources:


Primary:

Synology NAS


Runtime:

SQLite


Optional:

Vector database


---


## Model Layer


Supported:


Cloud:

- Gemini
- Claude
- OpenAI


Local:

- Ollama


The model layer must be replaceable.


---


# Example Workflow


User:

"Find my tax document"


Flow:


```
Telegram

↓

Agent Core

↓

Search Skill

↓

NAS Search Tool

↓

Document Found

↓

Telegram Response

```


# Editing Workflow


```
User Request

↓

Agent Planning

↓

Create Backup

↓

Copy File

↓

Execute Tool

↓

Validate

↓

Save

↓

Notify User

```