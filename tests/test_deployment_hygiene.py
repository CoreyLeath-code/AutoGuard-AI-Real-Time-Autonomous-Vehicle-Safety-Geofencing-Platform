"""Deployment-contract tests for Layer-7 traffic hygiene."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_raw_kubernetes_manifest_has_safe_http_rollout_contract():
    deployment = _read("infra/k8s/deployment.yaml")

    assert "type: RollingUpdate" in deployment
    assert "maxUnavailable: 0" in deployment
    assert "maxSurge: 1" in deployment
    assert "terminationGracePeriodSeconds: 30" in deployment
    assert "path: /health/live" in deployment
    assert "path: /health/ready" in deployment
    assert "startupProbe:" in deployment


def test_helm_values_and_template_render_the_same_rollout_contract():
    values = _read("infra/helm/autoguard/values.yaml")
    template = _read("infra/helm/autoguard/templates/deployment.yaml")

    assert "terminationGracePeriodSeconds: 30" in values
    assert "maxUnavailable: 0" in values
    assert "maxSurge: 1" in values
    assert ".Values.deployment.terminationGracePeriodSeconds" in template
    assert "toYaml .Values.deployment.strategy" in template
    assert "livenessProbe:" in template
    assert "readinessProbe:" in template
    assert "startupProbe:" in template
