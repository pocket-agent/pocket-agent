import asyncio
import logging

from uvicorn import Config, Server

from pocket_agent.interface.http_app import create_http_app
from pocket_agent.runtime.context import AgentRuntime

logger = logging.getLogger(__name__)


def _http_settings(runtime: AgentRuntime) -> dict:
    return runtime.settings.raw_settings.get("http", {})


async def run_http_server(runtime: AgentRuntime) -> None:
    cfg = _http_settings(runtime)
    host = cfg.get("host", "0.0.0.0")
    port = int(cfg.get("port", 8787))

    app = create_http_app(runtime)
    static_dir = app.state.static_dir
    if static_dir:
        logger.info("Serving web UI from %s", static_dir)
    else:
        logger.info("Web static dir not found — API only (build apps/web first)")

    config = Config(app=app, host=host, port=port, log_level="info")
    server = Server(config)
    logger.info("HTTP API listening on http://%s:%s", host, port)
    await server.serve()
