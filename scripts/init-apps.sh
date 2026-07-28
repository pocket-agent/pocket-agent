#!/usr/bin/env bash
# Clone pocket-agent app repos into apps/ (nested git projects).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ONLY="${1:-all}"
FORCE="${2:-}"

if command -v pocket-agent >/dev/null 2>&1; then
  ARGS=(init --only "$ONLY")
  if [[ "$FORCE" == "--force" ]]; then
    ARGS+=(--force)
  fi
  exec pocket-agent "${ARGS[@]}"
fi

if [[ -d .venv ]]; then
  exec .venv/bin/python -m pocket_agent.cli.init_apps --only "$ONLY" ${FORCE:+"--force"}
fi

exec python3 -m pocket_agent.cli.init_apps --only "$ONLY" ${FORCE:+"--force"}
