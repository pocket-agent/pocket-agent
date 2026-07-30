import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from pocket_agent.interface.auth import AuthError, resolve_user_claims
from pocket_agent.runtime.context import AgentRuntime

try:
    from pocket_agent_sdk import SERVICE_IDS
except ImportError:
    SERVICE_IDS = {"pocket_node": "pocket-agent", "api_worker": "pocket-agent-api"}

logger = logging.getLogger(__name__)


def _ok(data: Any) -> JSONResponse:
    return JSONResponse({"success": True, "data": data})


def _err(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse({"success": False, "message": message}, status_code=status_code)


def _http_config(runtime: AgentRuntime) -> dict:
    return runtime.settings.raw_settings.get("http", {})


def _allowed_origins(runtime: AgentRuntime) -> list[str]:
    cfg = _http_config(runtime)
    origins = cfg.get("allowed_origins", [])
    if isinstance(origins, list) and origins:
        return origins
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


def _static_dir(runtime: AgentRuntime) -> Path | None:
    cfg = _http_config(runtime)
    if not cfg.get("serve_static", True):
        return None
    rel = cfg.get("static_dir", "../pocket-agent-web-app/dist")
    path = Path(rel)
    if not path.is_absolute():
        path = (runtime.project_root / rel).resolve()
    if path.is_dir() and (path / "index.html").is_file():
        return path
    return None


async def health(_: Request) -> JSONResponse:
    return _ok(
        {
            "status": "ok",
            "timestamp": datetime.now(UTC).isoformat(),
            "service": SERVICE_IDS["pocket_node"],
        }
    )


async def status(request: Request) -> JSONResponse:
    runtime: AgentRuntime = request.app.state.runtime
    paths = runtime.settings.paths
    return _ok(
        {
            "agent": runtime.settings.raw_settings.get("agent", {}).get("name", "pocket-agent"),
            "llm_providers": runtime.llm_router.available_providers,
            "memory_count": runtime.memory.personal.count(),
            "knowledge_chunks": runtime.memory.knowledge.count(),
            "embeddings": runtime.memory.embeddings_available,
            "nas_root": str(paths.nas_root),
            "telegram_configured": bool(runtime.settings.env.telegram_bot_token),
        }
    )


def _require_user(request: Request) -> dict:
    runtime: AgentRuntime = request.app.state.runtime
    return resolve_user_claims(request.headers.get("authorization"), runtime.settings.env)


async def me(request: Request) -> JSONResponse:
    try:
        claims = _require_user(request)
    except AuthError as exc:
        return _err(str(exc), exc.status_code)

    return _ok(
        {
            "id": claims.get("sub"),
            "email": claims.get("email"),
            "user_metadata": claims.get("user_metadata", {}),
            "app_metadata": claims.get("app_metadata", {}),
            "created_at": claims.get("created_at"),
        }
    )


async def settings_llm_get(request: Request) -> JSONResponse:
    runtime: AgentRuntime = request.app.state.runtime
    try:
        providers = await runtime.llm_router.describe_providers()
        installed = await runtime.llm_router.list_ollama_models()
        return _ok(
            {
                "active_provider": runtime.llm_router.active_reasoning_provider(),
                "active_model": runtime.llm_router.reasoning_model(),
                "providers": providers,
                "ollama_installed_models": installed,
                "ollama_recommended": runtime.llm_router.recommended_ollama_models(),
            }
        )
    except Exception as exc:
        logger.exception("settings llm get failed")
        return _err(str(exc), 500)


async def settings_llm_post(request: Request) -> JSONResponse:
    runtime: AgentRuntime = request.app.state.runtime
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return _err("Invalid JSON body")

    try:
        if body.get("provider"):
            runtime.llm_router.set_reasoning_provider(str(body["provider"]))
        if body.get("ollama_model"):
            runtime.llm_router.set_ollama_model(str(body["ollama_model"]))
        if body.get("pull_ollama_model"):
            await runtime.llm_router.pull_ollama_model(str(body["pull_ollama_model"]))
    except ValueError as exc:
        return _err(str(exc), 400)
    except RuntimeError as exc:
        return _err(str(exc), 503)
    except Exception as exc:
        logger.exception("settings llm post failed")
        return _err(str(exc), 500)

    return await settings_llm_get(request)


async def chat(request: Request) -> JSONResponse:
    runtime: AgentRuntime = request.app.state.runtime
    try:
        claims = _require_user(request)
    except AuthError as exc:
        return _err(str(exc), exc.status_code)

    try:
        body = await request.json()
    except json.JSONDecodeError:
        return _err("Invalid JSON body")

    message = (body.get("message") or "").strip()
    if not message:
        return _err("message is required")

    history = body.get("history") or []
    user_key = str(claims.get("sub") or "local")
    chat_id = int(user_key) if user_key.isdigit() else None

    try:
        reply = await runtime.agent.handle_chat_message(
            message,
            history=history,
            chat_id=chat_id,
            user_key=user_key,
        )
        model = runtime.llm_router.reasoning_model()
        return _ok(
            {
                "message": message,
                "reply": reply,
                "model": model,
            }
        )
    except RuntimeError as exc:
        logger.exception("chat failed")
        return _err(str(exc), 503)
    except Exception as exc:
        logger.exception("chat failed")
        return _err(str(exc), 500)


async def spa_fallback(request: Request) -> Response:
    static_dir: Path = request.app.state.static_dir
    path = request.path_params.get("path", "")
    if path.startswith("api/"):
        return _err("Not found", 404)

    candidate = static_dir / path
    if path and candidate.is_file():
        return FileResponse(candidate)

    return FileResponse(static_dir / "index.html")


def create_http_app(runtime: AgentRuntime) -> Starlette:
    static_dir = _static_dir(runtime)
    routes: list = [
        Route("/health", health, methods=["GET"]),
        Route("/status", status, methods=["GET"]),
        Route("/me", me, methods=["GET"]),
        Route("/settings/llm", settings_llm_get, methods=["GET"]),
        Route("/settings/llm", settings_llm_post, methods=["POST"]),
        Route("/chat", chat, methods=["POST"]),
    ]

    if static_dir is not None:
        assets = static_dir / "assets"
        if assets.is_dir():
            routes.append(Mount("/assets", StaticFiles(directory=assets), name="assets"))
        routes.append(Route("/{path:path}", spa_fallback, methods=["GET"]))

    app = Starlette(routes=routes)
    app.state.runtime = runtime
    app.state.static_dir = static_dir

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(runtime),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
