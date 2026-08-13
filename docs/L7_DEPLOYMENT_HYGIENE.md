# Layer-7 Deployment Hygiene

## Scope

This document covers HTTP traffic handling for the prototype API deployment. It does not establish vehicle-control safety, a hard real-time guarantee, or availability SLOs.

## Readiness and shutdown

- `GET /health/live` reports process liveness.
- `GET /health/ready` reports `200` only while the application is accepting traffic.
- During application shutdown, the FastAPI lifespan marks the process as draining. The readiness endpoint then returns `503 draining` with `Retry-After: 5`.
- This signal is an application-level traffic-hygiene mechanism. It does not verify external dependencies or guarantee that every load balancer has removed the endpoint.

## Deployment contract

Both the raw Kubernetes manifest and Helm chart specify:

| Control | Setting | Purpose |
|---|---:|---|
| Rolling update | `maxUnavailable: 0`, `maxSurge: 1` | Preserve existing ready replicas while adding one replacement |
| Termination grace | 30 seconds | Allow ordinary HTTP shutdown to finish before forceful termination |
| Startup probe | `/health/live` | Prevent liveness restarts during initialization |
| Liveness probe | `/health/live` | Detect a nonresponsive process |
| Readiness probe | `/health/ready` | Remove a draining process from new traffic |

The configured values are defaults for a prototype. They must be calibrated against measured request duration, upstream timeout, replica count, and platform behavior before deployment.

## CI checks

`tests/test_api.py` verifies drain-aware readiness. `tests/test_deployment_hygiene.py` verifies that raw Kubernetes and Helm sources contain the same Layer-7 probe and rollout contract. These source-level tests do not replace `helm template`, admission-policy validation, staged rollout observation, or a real load-balancer test.
