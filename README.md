# AutoGuard-AI

[![CI](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform?display_name=tag&sort=semver)](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/releases)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-3776AB)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f)](LICENSE)
[![Scope: prototype](https://img.shields.io/badge/scope-prototype%20%2F%20simulation%20only-6b7280)](#safety-and-intended-use)

AutoGuard-AI is a Python prototype containing a radius-geofence implementation, a telemetry API, benchmark fixtures, and related research/development components. The release package is `autoguard-ai` and supports Python 3.11–3.12.

> **Safety boundary:** this is not an autonomous-vehicle safety system. It has not been validated on a vehicle, connected to actuators or braking hardware, shown to meet real-time requirements, or developed as a safety-certified product. Do not use it to make a safety-critical vehicle-control decision.

## What is implemented

| Area | Current behavior | Explicitly not established |
|---|---|---|
| Geometry | In-memory Haversine great-circle distance and inclusive radius predicate | Polygon, road-aware, or uncertainty-aware containment |
| API | FastAPI request validation, health/readiness endpoints, Prometheus metrics | Vehicle integration, safety authorization, or availability SLO |
| External geocoding adapter | Five-second HTTP timeout and conservative false fallback | Deterministic geofence membership; it must not be a safety boundary |
| Supervisor | Mock demonstration rules | Collision avoidance, braking, or hardware control |
| Benchmarks | Reproducible microbenchmark fixtures for geometry/serialization | Vehicle, network, or end-to-end timing claims |

The formal radius predicate is `inside(point, centre, radius) = distance(point, centre) <= radius`, where `distance` is Haversine great-circle distance using an Earth-radius constant of 6,371,000 metres. See [the implementation](libs/geofence/google_maps_geofence.py), [geometry tests](tests/test_geofence_unit.py), and [mathematical foundations](docs/MATHEMATICAL_FOUNDATIONS.md).

## Quickstart

Clone a tagged release for a repeatable starting point, then create an isolated environment:

```bash
git clone https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform.git
cd AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform
git checkout v0.1.0
python3.11 -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

Run the verified test suite and start the local API:

```bash
PYTHONPATH=. pytest tests --ignore=tests/benchmarks --cov=. --cov-fail-under=85
PYTHONPATH=. uvicorn services.api.main:app --host 127.0.0.1 --port 8000
```

In a second terminal, verify the non-safety health contract:

```bash
curl http://127.0.0.1:8000/health/ready
curl http://127.0.0.1:8000/metrics
```

The `/predict` endpoint validates telemetry fields and invokes a prototype external adapter. It is not a vehicle-control interface.

## Installable package

The core distribution deliberately does **not** compile CUDA code or install Torch. This keeps the prototype package installable on ordinary CPU development hosts.

```bash
python -m pip install .
python -m pip install ".[test]"   # test and benchmark dependencies
python -m pip install ".[full]"   # optional dashboard, ML, streaming, and experiment dependencies
```

Build and inspect the same artifacts published by the release workflow:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
sha256sum dist/*
```

The release workflow uploads the source distribution, universal wheel, checksum manifest, JUnit test result, coverage report, and GitHub build provenance attestation. Verify a downloaded artifact with the release `SHA256SUMS` file before use.

Tag releases also publish the API and dashboard images to GitHub Container Registry as `ghcr.io/coreyleath-code/autoguard-api:<tag>` and `ghcr.io/coreyleath-code/autoguard-dashboard:<tag>`. These images are prototype development artifacts, not approved vehicle-deployment images.

## Reproducibility and evidence

Release evidence is evidence for the tagged source and environment only; it is not performance, safety, accuracy, or vehicle-validation evidence.

| Evidence | How it is produced | Where to inspect it |
|---|---|---|
| Unit/integration tests | `PYTHONPATH=. pytest tests --ignore=tests/benchmarks --cov=. --cov-fail-under=85` | Release `pytest-results.xml` and `coverage.xml` |
| Package integrity | `python -m build && python -m twine check dist/*` | Release wheel/source archive and `SHA256SUMS` |
| Build provenance | GitHub Actions attestation on release distributions | GitHub release attestation |
| Geometry microbenchmarks | `pytest tests/benchmarks/test_geofence_benchmark.py --benchmark-only --benchmark-json=benchmarks/latest.json` | Generated raw JSON; no numeric result is committed as a product claim |

The exact release gate, local-validation notes, verification procedure, and current limits are in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md). The [verification scope](docs/VERIFICATION_SCOPE.md) defines claims that must remain `NOT IMPLEMENTED` until code and tests exist.

The release-readiness assessment and remaining blockers are documented in [docs/AUDIT_2026-08-21.md](docs/AUDIT_2026-08-21.md).

`metrics.py` produces synthetic demonstration data (random samples, sleeps, and hard-coded values). It is not benchmark, quality, or safety evidence.

## Architecture

```text
telemetry request
      |
      v
FastAPI validation ──> async thread offload ──> prototype geocoding adapter
      |                                                   |
      +--> health / readiness / Prometheus metrics         +--> boolean response

independent: Haversine distance + radius predicate <── geometry unit tests / microbenchmarks
```

See [docs/architecture.md](docs/architecture.md) for component-level detail. Infrastructure manifests, Docker files, ML experiments, and dashboards are development assets; their presence does not establish a production deployment or safety capability.

## Configuration and data handling

Copy `.env.example` and set only the values needed for local development. Never commit `.env`, API keys, kubeconfigs, private certificates, or generated datasets. The current API reads `GOOGLE_API_KEY`, geofence centre/radius, logging, and optional service endpoints from environment variables; see [services/api/config.py](services/api/config.py).

The project has no committed dataset, model card, privacy assessment, retention policy, or vehicle-data authorization. Treat telemetry as potentially sensitive and keep it out of issue text, logs, and public artifacts.

## Safety and intended use

Permitted use is local development, code review, experimentation, and simulation/research with appropriate controls. Excluded use includes vehicle control, braking decisions, claims of real-time operation, safety certification, and claims of geofence/perception quality without independent evidence.

Known limitations include GPS uncertainty, spherical-radius-only geometry, an external text-dependent geocoding adapter, no offline geospatial oracle, no fault-injection campaign, no hazard analysis, no safety case, and no independent verification. The detailed assessment is in [docs/ACADEMIC_AUDIT.md](docs/ACADEMIC_AUDIT.md).

## Development and contribution

Use the focused CI dependency set for repository work:

```bash
python -m pip install -r requirements-ci.txt
PYTHONPATH=. pytest tests --ignore=tests/benchmarks
```

Before opening a change, run tests, build the distribution if package metadata changes, and avoid adding unmeasured capability claims. See [CONTRIBUTING.md](CONTRIBUTING.md), [docs/development.md](docs/development.md), and the open [production-readiness audit](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/issues/14).

## Security

Report suspected credential exposure privately to the repository owner; do not post secrets in a public issue. CI runs formatting, type, and Bandit checks. Dependency, secret, container, and deployment controls still require periodic independent review before any broader use.

## License

This project is released under the [MIT License](LICENSE).
