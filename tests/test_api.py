"""FastAPI endpoint tests for services/api/main.py."""

from prometheus_client import REGISTRY


def test_liveness_probe(api_client):
    response = api_client.get("/health/live")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "alive"
    assert "uptime_seconds" in body


def test_readiness_probe(api_client):
    response = api_client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_legacy_health_endpoint(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200


def test_health_uptime_is_non_negative(api_client):
    response = api_client.get("/health/live")
    assert response.json()["uptime_seconds"] >= 0


def test_predict_valid_payload(api_client, telemetry_payload):
    response = api_client.post("/predict", json=telemetry_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["vehicle_id"] == "VH-001"
    assert body["geofence_valid"] is True
    assert body["latency_ms"] >= 0


def test_predict_geofence_valid_is_bool(api_client):
    payload = {"lat": 40.0, "lon": -83.0, "vehicle_id": "VH-BOOL"}
    response = api_client.post("/predict", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json()["geofence_valid"], bool)


def test_predict_validation_errors(api_client):
    invalid_payloads = [
        {"lat": 40.0, "lon": -83.0},
        {"lat": 40.0, "lon": -83.0, "vehicle_id": ""},
        {"lat": 200.0, "lon": -83.0, "vehicle_id": "VH-002"},
        {"lat": 40.0, "lon": 999.0, "vehicle_id": "VH-003"},
        {"lat": 40.0, "lon": -83.0, "speed": -5.0, "vehicle_id": "VH-NEG"},
    ]

    for payload in invalid_payloads:
        assert api_client.post("/predict", json=payload).status_code == 422


def test_predict_accepts_coordinate_boundaries(api_client):
    valid_payloads = [
        {"lat": 90.0, "lon": 0.0, "vehicle_id": "VH-MAXLAT"},
        {"lat": -90.0, "lon": 0.0, "vehicle_id": "VH-MINLAT"},
        {"lat": 0.0, "lon": 180.0, "vehicle_id": "VH-MAXLON"},
        {"lat": 0.0, "lon": -180.0, "vehicle_id": "VH-MINLON"},
    ]

    for payload in valid_payloads:
        assert api_client.post("/predict", json=payload).status_code == 200


def test_metrics_endpoint(api_client):
    response = api_client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text


def test_request_id_header_present(api_client):
    response = api_client.get("/health/live")
    assert "x-request-id" in response.headers


def test_predict_increments_request_counter(api_client):
    before = REGISTRY.get_sample_value("api_requests_total") or 0.0
    payload = {"lat": 40.0, "lon": -83.0, "vehicle_id": "VH-CTR"}
    api_client.post("/predict", json=payload)
    after = REGISTRY.get_sample_value("api_requests_total") or 0.0
    assert after > before



def test_readiness_returns_503_while_draining(api_client, monkeypatch):
    from services.api.main import app

    monkeypatch.setattr(app.state, "accepting_traffic", False)
    response = api_client.get("/health/ready")

    assert response.status_code == 503
    assert response.text == "draining"
    assert response.headers["retry-after"] == "5"
