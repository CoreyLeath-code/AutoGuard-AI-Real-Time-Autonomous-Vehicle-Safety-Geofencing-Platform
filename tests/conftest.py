"""Shared pytest fixtures for AutoGuard's lightweight CI test suite."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def telemetry_payload() -> dict[str, object]:
    return {"lat": 40.0, "lon": -83.0, "speed": 10.0, "vehicle_id": "VH-001"}


@pytest.fixture
def api_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """FastAPI client with the external geofence lookup isolated."""
    from services.api.main import app

    monkeypatch.setattr("services.api.main.check_geofence", lambda lat, lon: True)
    return TestClient(app)
