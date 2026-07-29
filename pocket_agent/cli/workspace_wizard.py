"""Local setup wizard server — liquid-glass UI + module install API."""

from __future__ import annotations

import json
import logging
import webbrowser
from pathlib import Path

import uvicorn
import yaml
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from pocket_agent.cli.init_modules import install_module, load_modules_config
from pocket_agent.cli.setup_wizard import run_setup
from pocket_agent.cli.workspace_bootstrap import check_prerequisites, run_bootstrap
from pocket_agent.workspace.paths import find_workspace_root

logger = logging.getLogger(__name__)

DEFAULT_PORT = 8790


def _wizard_dist(workspace: Path) -> Path:
    return workspace / "wizard" / "dist"


def _module_status(workspace: Path) -> list[dict]:
    config = load_modules_config(workspace)
    modules = config.get("modules", {})
    items: list[dict] = []
    for name, spec in modules.items():
        rel = spec.get("path", f"pocket-agent-{name}")
        path = workspace / rel
        installed = path.is_dir() and any(path.iterdir()) if path.exists() else False
        items.append(
            {
                "name": name,
                "path": rel,
                "github": spec.get("github"),
                "description": spec.get("description", ""),
                "enabled": spec.get("enabled", True),
                "installed": installed,
            }
        )
    return items


async def api_modules(request: Request) -> JSONResponse:
    workspace = find_workspace_root()
    return JSONResponse({"modules": _module_status(workspace)})


async def api_setup_get(request: Request) -> JSONResponse:
    workspace = find_workspace_root()
    setup_path = workspace / "config" / "user-setup.yaml"
    defaults_path = workspace / "config" / "setup.defaults.yaml"
    data: dict = {}
    if defaults_path.is_file():
        with defaults_path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    if setup_path.is_file():
        with setup_path.open(encoding="utf-8") as fh:
            user = yaml.safe_load(fh) or {}
            data = {**data, **user}
    return JSONResponse(data)


async def api_setup_post(request: Request) -> JSONResponse:
    body = await request.json()
    workspace = find_workspace_root()
    profile = body.get("profile")
    overrides: dict = {}

    module_modes = body.get("modules") or {}
    urls = body.get("urls") or {}
    for name, mode in module_modes.items():
        if name not in ("web", "api"):
            continue
        if mode == "remote":
            overrides[name] = {"mode": "remote", "url": urls.get(name, "")}
        else:
            overrides[name] = {"mode": "local"}

    if body.get("google_oauth", {}).get("client_id"):
        overrides["google_oauth"] = body["google_oauth"]

    if body.get("ui", {}).get("primary"):
        overrides["ui"] = body["ui"]

    code = run_setup(
        workspace_root=workspace,
        force=True,
        profile=profile,
        overrides=overrides if overrides else None,
    )
    if code != 0:
        return JSONResponse({"ok": False}, status_code=500)
    return JSONResponse({"ok": True})


async def api_install_post(request: Request) -> JSONResponse:
    body = await request.json()
    names = body.get("modules") or []
    source = body.get("source", "release")
    force = bool(body.get("force", False))
    workspace = find_workspace_root()
    config = load_modules_config(workspace)
    module_specs = config.get("modules", {})
    results: list[str] = []

    for name in names:
        if name not in module_specs:
            results.append(f"error:{name}:unknown")
            continue
        try:
            result = install_module(
                name,
                module_specs[name],
                workspace,
                force=force,
                source=source if source in ("release", "git") else "release",
            )
            results.append(result)
        except Exception as exc:
            logger.exception("Install failed for %s", name)
            results.append(f"error:{name}:{exc}")

    return JSONResponse({"results": results, "modules": _module_status(workspace)})


async def api_prereqs(request: Request) -> JSONResponse:
    workspace = find_workspace_root()
    return JSONResponse(check_prerequisites(workspace))


async def api_bootstrap_post(request: Request) -> JSONResponse:
    body = await request.json()
    workspace = find_workspace_root()
    use_desktop = bool(body.get("use_desktop", False))
    google = body.get("google_oauth") or {}
    result = run_bootstrap(
        workspace_root=workspace,
        google_client_id=google.get("client_id"),
        gemini_api_key=body.get("gemini_api_key"),
        use_desktop=use_desktop,
        generate_icons=use_desktop,
    )
    return JSONResponse(result)


def build_wizard_app(workspace: Path) -> Starlette:
    dist = _wizard_dist(workspace)
    routes: list = [
        Route("/api/modules", api_modules),
        Route("/api/setup", api_setup_get, methods=["GET"]),
        Route("/api/setup", api_setup_post, methods=["POST"]),
        Route("/api/install", api_install_post, methods=["POST"]),
        Route("/api/prereqs", api_prereqs),
        Route("/api/bootstrap", api_bootstrap_post, methods=["POST"]),
    ]

    if dist.is_dir():
        routes.append(Mount("/", StaticFiles(directory=str(dist), html=True), name="static"))
    else:
        routes.append(
            Route(
                "/",
                lambda request: JSONResponse(
                    {
                        "message": "Wizard UI not built. Run: cd wizard && bun install && bun run build",
                        "api": ["/api/modules", "/api/setup", "/api/install"],
                    }
                ),
            )
        )

    return Starlette(routes=routes)


def run_wizard_server(port: int = DEFAULT_PORT, open_browser: bool = True) -> int:
    workspace = find_workspace_root()
    app = build_wizard_app(workspace)
    url = f"http://127.0.0.1:{port}"
    logger.info("Workspace wizard at %s (workspace: %s)", url, workspace)

    if open_browser:
        webbrowser.open(url)

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="pocket-agent wizard",
        description="Open the workspace setup wizard (liquid-glass UI)",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-open", action="store_true", help="Do not open browser")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return run_wizard_server(port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    import sys

    sys.exit(main())
