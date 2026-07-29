# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-29

### Added

- **Pocket Node** — Python agent with LLM routing (Gemini), tools, memory, and skills
- **CLI** — `serve`, `telegram`, `init`, `setup`, `wizard`, `bootstrap`
- **HTTP API** — `/health`, `/status`, `/me`, `/chat` with Google ID token verification
- **Workspace integration** — module install from GitHub releases, setup wizard server, env bootstrap across sibling apps
- **Telegram interface** — bot entry point for mobile chat
- **File safety pipeline** — backup → working copy → validate → replace for tool operations
- **Shared contracts** — consumes `pocket_agent_sdk` for connection profiles and service IDs

---

## Repository documents

[README](README.md) | [INSTRUCTIONS](INSTRUCTIONS.md) | **CHANGELOG** | [CONTRIBUTING](CONTRIBUTING.md) | [SECURITY](SECURITY.md) | [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)
