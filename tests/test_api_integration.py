"""Integration and regression tests for API request flow."""

from fastapi.testclient import TestClient

from services.api.main import app


def test_predict_uses_geofence_service_result(monkeypatch, telemetry_payload):
    calls = []

    def fake_check_geofence(lat, lon):
        calls.append((lat, lon))
        return False

    monkeypatch.setattr("services.api.main.check_geofence", fake_check_geofence)

    with TestClient(app) as client:
        response = client.post("/predict", json=telemetry_payload)

    assert response.status_code == 200
    assert response.json()["geofence_valid"] is False
    assert calls == [(40.0, -83.0)]


def test_predict_returns_502_when_geofence_service_fails(
    monkeypatch, telemetry_payload
):
    def failing_check_geofence(lat, lon):
        raise RuntimeError("upstream unavailable")

    monkeypatch.setattr("services.api.main.check_geofence", failing_check_geofence)

    with TestClient(app) as client:
        response = client.post("/predict", json=telemetry_payload)

    assert response.status_code == 502
    assert "Geofence check failed" in response.json()["detail"]
