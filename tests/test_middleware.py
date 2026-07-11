"""Middleware behavior tests."""

import json
import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.api.middleware import GlobalExceptionMiddleware, configure_logging


def test_configure_logging_emits_json_records():
    configure_logging("INFO")
    record = logging.LogRecord(
        name="autoguard.api",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="structured",
        args=(),
        exc_info=None,
    )
    formatted = logging.root.handlers[0].formatter.format(record)

    assert json.loads(formatted)["msg"] == "structured"


def test_global_exception_middleware_returns_structured_500():
    app = FastAPI()
    app.add_middleware(GlobalExceptionMiddleware)

    @app.get("/boom")
    async def boom():
        raise RuntimeError("unexpected")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/boom")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
