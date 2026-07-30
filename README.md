<img src=".github/pocket-agent-image.png" width="200" alt="Pocket Agent" align="left"/>

<div>
<h3>Pocket Node</h3>
<p>
Python Pocket Node for the open-source <strong>Pocket Agent</strong> ecosystem — LLM routing, tools, memory, Telegram, and the <code>pocket-agent serve</code> HTTP API on your machine.
</p>
<a href="https://github.com/pocket-agent/pocket-agent-desktop-app/releases"><img src="https://img.shields.io/badge/Download%20for%20macOS-007ec6?style=flat-square&logo=apple" width="175" alt="Download for macOS"/></a>
</div>

<br/><br/>

<div align="center">

[![Release](https://img.shields.io/github/v/release/pocket-agent/pocket-agent)](https://github.com/pocket-agent/pocket-agent/releases)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/pocket-agent/pocket-agent/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://github.com/pocket-agent/pocket-agent)
[![CI](https://github.com/pocket-agent/pocket-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/pocket-agent/pocket-agent/actions/workflows/ci.yml)

<br/>
<br/>

<img src=".github/screenshot.png" width="824" alt="Pocket Agent" style="border-radius: 5px;"/><br/>

</div>

<hr>

## Features

- **Pocket Node HTTP API** — `/health`, `/status`, `/me`, `/chat`, settings on `:8787`
- **CLI** — `serve`, `telegram`, `init`, `setup`, `wizard`, `bootstrap`
- **Tools & skills** — files, memory, weather, web fetch, calendar, reminders, utilities
- **LLM routing** — configurable providers (e.g. Ollama) and local dev with `AUTH_MODE=none`
- **Workspace integration** — install sibling modules, sync env files, setup wizard server
- **Shared contracts** — `pocket_agent_sdk` from [pocket-agent-sdk](https://github.com/pocket-agent/pocket-agent-sdk)

## Requirements

- **Python 3.12+**
- macOS or Linux for local development (desktop app targets macOS)

## Install

1. **End users:** download the all-in-one **Pocket Agent** app from [GitHub Releases](https://github.com/pocket-agent/pocket-agent-desktop-app/releases) or [pocket-agent.pages.dev](https://pocket-agent.pages.dev) (bundled Pocket Node).
2. **Developers:** clone this repo and install in a venv (see Development).

## Quick start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ../pocket-agent-sdk/python   # workspace sibling
pip install -e ".[dev]"
pocket-agent serve
```

Open `http://127.0.0.1:8787/health`. Full workspace: run `../scripts/setup-local.sh` from the org workspace, or `pocket-agent wizard` for the setup UI.

## Development

```bash
git clone https://github.com/pocket-agent/pocket-agent.git
cd pocket-agent
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

- Follow the spec-driven workflow in [INSTRUCTIONS.md](INSTRUCTIONS.md)
- Run tests via CI or local pytest (see [DEVELOPMENT.md](DEVELOPMENT.md))
- Sync branding assets across repos: `../scripts/sync-pocket-agent-branding.sh` (workspace)

## Documentation

| Doc | Description |
|-----|-------------|
| [DEVELOPMENT.md](DEVELOPMENT.md) | Local setup and testing |
| [INSTRUCTIONS.md](INSTRUCTIONS.md) | Agent development rules |
| [AGENT_PROTOCOL.md](AGENT_PROTOCOL.md) | HTTP and chat protocol |
| [TOOLS_SPEC.md](TOOLS_SPEC.md) | Tool definitions |
| [CHANGELOG.md](CHANGELOG.md) | Release history |

Ecosystem: [pocket-agent](https://github.com/pocket-agent) · Creator: [Charlie Rios (@xarlizard)](https://github.com/xarlizard)

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

To report a vulnerability, see [SECURITY.md](SECURITY.md).

## License

Pocket Node is released under the [MIT License](LICENSE).
