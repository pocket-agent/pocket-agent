# Pocket Agent Architecture


# Overview


Pocket Agent consists of six layers.


## Interface Layer

Responsible for user communication.


Current:

- Telegram


Future:

- Web dashboard
- Mobile apps


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