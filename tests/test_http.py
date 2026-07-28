import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from starlette.testclient import TestClient

from pocket_agent.config.models import AppSettings, LlmConfig, PathsConfig, SettingsBundle
from pocket_agent.interface.http_app import create_http_app
from pocket_agent.runtime.context import AgentRuntime


def _runtime(tmp_path: Path, jwt_secret: str = "test-secret") -> AgentRuntime:
    nas = tmp_path / "nas"
    nas.mkdir()

    paths = PathsConfig(
        {
            "nas": {"root": str(nas), "allowed_read_roots": [str(nas)]},
            "data": {"logs": "data/logs"},
        },
        tmp_path,
    )
    paths.logs_dir.mkdir(parents=True, exist_ok=True)

    env = AppSettings(
        SUPABASE_JWT_SECRET=jwt_secret,
        SUPABASE_JWT_AUDIENCE="authenticated",
    )
    llm = LlmConfig({"default_provider": "gemini", "providers": {}})
    settings = SettingsBundle(
        env,
        paths,
        llm,
        {
            "agent": {"name": "pocket-agent"},
            "http": {"serve_static": False},
        },
    )

    agent = MagicMock()
    agent.handle_chat_message = AsyncMock(return_value="Agent reply")

    llm_router = MagicMock()
    llm_router.available_providers = ["gemini"]
    llm_router.reasoning_model = MagicMock(return_value="gemini-2.0-flash")

    memory = MagicMock()
    memory.personal.count = MagicMock(return_value=2)
    memory.knowledge.count = MagicMock(return_value=5)
    memory.embeddings_available = True

    return AgentRuntime(
        settings=settings,
        project_root=tmp_path,
        llm_router=llm_router,
        memory=memory,
        agent=agent,
    )


def _token(secret: str, sub: str = "user-abc") -> str:
    payload = {
        "sub": sub,
        "email": "user@example.com",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
        "user_metadata": {"name": "Test"},
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def test_health_endpoint(tmp_path: Path):
    runtime = _runtime(tmp_path)
    with TestClient(create_http_app(runtime)) as client:
        response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert body["data"]["service"] == "pocket-agent"


def test_status_endpoint(tmp_path: Path):
    runtime = _runtime(tmp_path)
    with TestClient(create_http_app(runtime)) as client:
        response = client.get("/status")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["agent"] == "pocket-agent"
    assert body["data"]["memory_count"] == 2


def test_me_requires_auth(tmp_path: Path):
    runtime = _runtime(tmp_path)
    with TestClient(create_http_app(runtime)) as client:
        response = client.get("/me")

    assert response.status_code == 401


def test_me_with_valid_jwt(tmp_path: Path):
    runtime = _runtime(tmp_path)
    token = _token("test-secret")
    with TestClient(create_http_app(runtime)) as client:
        response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == "user-abc"
    assert body["data"]["email"] == "user@example.com"


def test_chat_with_valid_jwt(tmp_path: Path):
    runtime = _runtime(tmp_path)
    token = _token("test-secret")
    with TestClient(create_http_app(runtime)) as client:
        response = client.post(
            "/chat",
            headers={"Authorization": f"Bearer {token}"},
            json={"message": "Hi", "history": [{"role": "user", "content": "Earlier"}]},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["reply"] == "Agent reply"
    assert body["data"]["model"] == "gemini-2.0-flash"
    runtime.agent.handle_chat_message.assert_awaited_once()
    call_kwargs = runtime.agent.handle_chat_message.await_args.kwargs
    assert call_kwargs["history"] == [{"role": "user", "content": "Earlier"}]
