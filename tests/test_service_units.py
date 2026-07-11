"""Unit tests for service adapters and external-boundary mocking."""

from __future__ import annotations

import importlib
import json
import sys
from types import SimpleNamespace

import pytest
import requests


class _Response:
    def __init__(self, payload=None, exc: Exception | None = None):
        self.payload = payload
        self.exc = exc

    def raise_for_status(self):
        if self.exc:
            raise self.exc

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


def test_check_geofence_returns_false_without_api_key(monkeypatch):
    import services.api.geofence as geofence

    monkeypatch.setattr(geofence, "GOOGLE_API_KEY", "")
    assert geofence.check_geofence(40.0, -83.0) is False


def test_check_geofence_allows_ohio_result(monkeypatch):
    import services.api.geofence as geofence

    monkeypatch.setattr(geofence, "GOOGLE_API_KEY", "token")
    monkeypatch.setattr(
        geofence.requests,
        "get",
        lambda url, timeout: _Response(
            {"results": [{"formatted_address": "Columbus, Ohio"}]}
        ),
    )

    assert geofence.check_geofence(40.0, -83.0) is True


def test_check_geofence_rejects_empty_non_ohio_and_bad_responses(monkeypatch):
    import services.api.geofence as geofence

    monkeypatch.setattr(geofence, "GOOGLE_API_KEY", "token")

    for response in [
        _Response({"results": []}),
        _Response({"results": [{"formatted_address": "Detroit, Michigan"}]}),
        _Response(ValueError("bad json")),
        _Response({"results": []}, requests.Timeout("slow")),
    ]:
        monkeypatch.setattr(
            geofence.requests, "get", lambda url, timeout, r=response: r
        )
        assert geofence.check_geofence(40.0, -83.0) is False


def test_ab_testing_selects_expected_model(monkeypatch):
    from services.api import ab_testing

    monkeypatch.setattr(ab_testing.random, "random", lambda: 0.79)
    assert ab_testing.select_model() == "model_v1"

    monkeypatch.setattr(ab_testing.random, "random", lambda: 0.80)
    assert ab_testing.select_model() == "model_v2"


def test_load_balancer_routes_to_selected_server(monkeypatch):
    from services.api import load_balancer

    payload = {"vehicle_id": "VH-ROUTE"}
    calls = []

    monkeypatch.setattr(load_balancer.random, "choice", lambda servers: servers[1])
    monkeypatch.setattr(
        load_balancer.requests,
        "post",
        lambda server, json: calls.append((server, json)) or _Response({"ok": True}),
    )

    assert load_balancer.route_request(payload) == {"ok": True}
    assert calls == [(load_balancer.INFERENCE_SERVERS[1], payload)]


def test_redis_cache_serializes_keys_and_payloads(monkeypatch):
    stored = {}

    class FakeRedisClient:
        def get(self, key):
            return stored.get(key)

        def setex(self, key, ttl, value):
            stored[key] = value
            stored[f"{key}:ttl"] = ttl

    fake_client = FakeRedisClient()
    fake_redis_module = SimpleNamespace(Redis=lambda **kwargs: fake_client)
    monkeypatch.setitem(sys.modules, "redis", fake_redis_module)
    sys.modules.pop("services.api.redis_cache", None)

    redis_cache = importlib.import_module("services.api.redis_cache")
    payload = {"lon": -83.0, "lat": 40.0}
    same_payload_different_order = {"lat": 40.0, "lon": -83.0}
    response = {"geofence_valid": True}

    assert redis_cache.cache_key(payload) == redis_cache.cache_key(
        same_payload_different_order
    )
    assert redis_cache.get_cached(payload) is None

    redis_cache.set_cache(payload, response)
    key = redis_cache.cache_key(payload)

    assert stored[f"{key}:ttl"] == 60
    assert json.loads(stored[key]) == response
    assert redis_cache.get_cached(payload) == response


def test_settings_read_environment_at_import(monkeypatch):
    import services.api.config as config

    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("GEOFENCE_RADIUS_M", "123.5")

    reloaded = importlib.reload(config)

    assert reloaded.settings.api_port == 9000
    assert reloaded.settings.log_level == "DEBUG"
    assert reloaded.settings.geofence_radius_m == 123.5

    monkeypatch.delenv("API_PORT")
    monkeypatch.delenv("LOG_LEVEL")
    monkeypatch.delenv("GEOFENCE_RADIUS_M")
    importlib.reload(config)
