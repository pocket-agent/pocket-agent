---
type: Feature
title: Purpose
description: Private, self-hosted personal AI assistant on user-owned infrastructure.
tags: [vision, pocket-agent]
timestamp: 2026-07-28T00:00:00Z
---

Pocket Agent is a personal automation system that runs continuously on private hardware, connected to personal files, tools, and workflows.

## Goals

- Search and understand personal documents
- Edit PDFs, Excel, and documents safely
- Manage personal knowledge and memory
- Automate repetitive workflows
- Communicate through Telegram
- Operate as a 24/7 assistant

## What it is not

A chatbot. Pocket Agent is a personal AI operating system combining LLM reasoning, local tools, skills, memory, automation, and external integrations — with the user owning infrastructure, data, and workflows.

## Core constraints

- **Private first** — personal files stay on private infrastructure; external APIs only when required
- **Tool-based execution** — the LLM reasons; tools execute; never direct LLM file modification
- **Safe file operations** — backups, logs, rollback, validation before destructive changes

## Canonical docs

- [README.md](../../README.md) — vision and capabilities
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — system layers
- [ROADMAP.md](../../ROADMAP.md) — phased delivery
