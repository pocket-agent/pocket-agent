# Features (contract)

| Feature | Surface | Auth |
|---------|---------|------|
| Health | `GET /health` | Public |
| Status | `GET /status` | Public |
| Chat | `POST /chat` | Local bypass or Bearer |
| Me / settings | `/me`, `/settings/*` | Local bypass or Bearer |
| CLI | `pocket-agent serve`, `init`, `wizard`, `bootstrap` | Local env |
| Tools | Agent skills (files, memory, web, calendar, …) | Agent policy |
| Workspace bootstrap | Sync env to `pocket-agent-app` | Maintainer |

See numbered specs under `specs/features/`.
