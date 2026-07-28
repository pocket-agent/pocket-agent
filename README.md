# Pocket Agent

Your private, self-hosted AI assistant.

Pocket Agent is a personal automation system designed to run continuously on your own hardware, connected to your private files, tools, and workflows.

The goal is to create a personal AI agent capable of:

- Searching personal documents
- Understanding files
- Editing PDFs
- Editing Excel spreadsheets
- Creating and modifying documents
- Managing personal knowledge
- Automating repetitive workflows
- Communicating through Telegram
- Running continuously as a 24/7 assistant


## Vision

Pocket Agent is not a chatbot.

It is a personal AI operating system.

The system combines:

- LLM reasoning
- Local tools
- Personal files
- Skills
- Memory
- Automation workflows
- External integrations

The user owns the infrastructure, data, and workflows.


## Development

Phase 1 foundation is scaffolded. See [DEVELOPMENT.md](DEVELOPMENT.md) for setup (Python 3.12+, Telegram, Gemini).

Monorepo clients: [apps/](apps/) — `web` (Pages), `api` (Worker), `desktop` (Tauri), `cli` (future).

```bash
pip install -e ".[dev]"
pocket-agent init    # clone pocket-agent-web-app + pocket-agent-api-app
pocket-agent serve   # Pocket Node HTTP API
```

Architecture: [docs/APPS_ARCHITECTURE.md](docs/APPS_ARCHITECTURE.md)


# Main Architecture

```
                         User

                          |
                          |

                       Telegram

                          |
                          |

                 Pocket Agent Core

                          |
        -----------------------------------

        |                |                |

     Gemini API      Local LLM        Tool System

                         |

                    Ollama Runtime


                         |

                   Synology NAS

```


# Hardware


## Pocket Node

Primary runtime:

Mac Mini M1

Specifications:

- Apple Silicon M1
- 8GB RAM
- Always running
- Connected to Synology NAS


Responsibilities:

- Agent execution
- Telegram bot
- Scheduling
- File processing
- LLM routing
- Automation


## Development Machine

MacBook Pro M1 Max

Specifications:

- 32GB RAM
- Cursor IDE

Responsibilities:

- Development
- Testing
- Maintenance


## Storage

Synology NAS.

Used as:

- Main document storage
- Archive
- Knowledge source
- Backup location


# Core Principles


## Private First

Personal files remain on private infrastructure.

External APIs are used only when required.

The system should work with:

- Local models
- Cloud models
- Hybrid workflows


## Tool-Based Execution

The LLM should never directly manipulate files.

The correct architecture:

```
User Request

↓

LLM Reasoning

↓

Tool Selection

↓

Python Execution

↓

Validation

↓

Response
```


The LLM decides what should happen.

Tools decide how it happens.


## Safe File Operations

All modifications must:

- Create backups
- Generate logs
- Support rollback
- Validate output
- Avoid accidental destruction


# Capabilities


## File Intelligence

- File search
- Metadata extraction
- Document understanding
- Semantic search


## PDF

- Extract text
- Summarize documents
- Modify PDFs
- Generate PDFs


## Excel

- Read workbooks
- Analyze spreadsheets
- Modify cells
- Generate reports


## Documents

- Create documents
- Modify documents
- Format content


## Communication

- Telegram bot
- Notifications
- Commands
- Scheduled messages


# LLM Strategy

Pocket Agent supports multiple models.


Cloud providers:

- Google Gemini
- Anthropic Claude
- OpenAI


Local providers:

- Ollama
- Local open-source models


The system should route tasks intelligently.


Example:

```
Simple classification

↓

Local model


Complex reasoning

↓

Gemini


Coding task

↓

Claude
```


# Repository Structure


```
pocket-agent/

├── README.md
├── index.md
├── INSTRUCTIONS.md
├── ARCHITECTURE.md
├── SECURITY.md
├── DEVELOPMENT.md
├── ROADMAP.md
├── SKILLS.md
├── TOOLS_SPEC.md
├── AGENT_PROTOCOL.md

├── apps/                    # Client applications (monorepo)
│   ├── web/                 # React + Cloudflare Pages + Google OAuth
│   └── desktop/             # Tauri multi-platform app

├── src/pocket_agent/        # Python agent core

├── agent/                   # Runtime skills, prompts, memory
│   ├── skills/
│   ├── prompts/
│   └── memory/

├── config/
├── data/
└── tests/
```

Local installs serve `apps/web` from the Pocket Node without Cloudflare. Hosted deploy uses the same `apps/web` on Cloudflare Pages. `apps/desktop` wraps the UI in Tauri for desktop devices.


# Long Term Goal

Pocket Agent should become:

- A private AI assistant
- A personal automation platform
- A local-first alternative to cloud assistants
- A framework for building personal agents