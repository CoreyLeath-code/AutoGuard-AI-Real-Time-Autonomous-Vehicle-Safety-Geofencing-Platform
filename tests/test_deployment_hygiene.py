"""Deployment-contract tests for prototype HTTP traffic hygiene."""

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
    assert "initialDelaySeconds: 5" in deployment
    assert "failureThreshold: 3" in deployment
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


def test_raw_manifest_has_secure_runtime_and_capacity_contract():
    deployment = _read("infra/k8s/deployment.yaml")

    assert "serviceAccountName: autoguard-api" in deployment
    assert "runAsNonRoot: true" in deployment
    assert "allowPrivilegeEscalation: false" in deployment
    assert "readOnlyRootFilesystem: true" in deployment
    assert "        - ALL" in deployment
    assert "requests:" in deployment
    assert 'cpu: "500m"' in deployment
    assert "memory: 512Mi" in deployment
    assert "limits:" in deployment
    assert 'cpu: "2"' in deployment
    assert "memory: 2Gi" in deployment


def test_helm_values_enable_availability_and_network_controls():
    values = _read("infra/helm/autoguard/values.yaml")

    assert "replicaCount: 2" in values
    assert "autoscaling:\n  enabled: true" in values
    assert "minReplicas: 2" in values
    assert "pdb:\n  enabled: true" in values
    assert "minAvailable: 1" in values
    assert "networkPolicy:\n  enabled: true" in values
    assert "runAsNonRoot: true" in values
    assert "readOnlyRootFilesystem: true" in values


def test_helm_template_wires_health_security_and_capacity_values():
    template = _read("infra/helm/autoguard/templates/deployment.yaml")

    assert "toYaml .Values.livenessProbe" in template
    assert "toYaml .Values.readinessProbe" in template
    assert "toYaml .Values.startupProbe" in template
    assert "toYaml .Values.podSecurityContext" in template
    assert "toYaml .Values.securityContext" in template
    assert "toYaml .Values.resources" in template
    assert "serviceAccountName:" in template
