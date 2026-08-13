# AutoGuard-AI — Geofence Prototype and Telemetry API

[![CI](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/ci.yml)
[![SBOM](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/sbom.yml/badge.svg)](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/sbom.yml)
[![Trivy security scan](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/trivy.yml/badge.svg)](https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/actions/workflows/trivy.yml)
[![Python CI](https://img.shields.io/badge/Python_CI-3.11-3776AB)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f)](LICENSE)
[![Geofence method](https://img.shields.io/badge/geofence-Haversine_radius_predicate-6f42c1)](libs/geofence/google_maps_geofence.py)
[![Scope: prototype](https://img.shields.io/badge/scope-prototype_%2F_simulation_only-6b7280)](#safety-boundary)

## Safety boundary

AutoGuard-AI is a software prototype and simulation-oriented collection of geofencing, telemetry, API, and model-support code. It is **not** a deployable autonomous-vehicle safety system. It has not been validated on a vehicle, connected to braking hardware, demonstrated to meet a real-time deadline, or developed as a safety-certified product.

Nothing in this repository should be used to make a safety-critical vehicle-control decision. The prior README’s claims about hard real time, hardware circuit breakers, physical braking, vehicle-safety performance, throughput, and latency caps are not supported by a committed safety case or valid benchmark artifact and have been removed.

## Abstract

The directly implemented and tested geospatial method is an in-memory Haversine great-circle distance followed by an inclusive radius-membership decision. A FastAPI endpoint validates latitude, longitude, speed, and vehicle ID, then calls a separate prototype Google-geocoding integration. The local supervisor contains mock rule paths for demonstration, not collision avoidance or vehicle control.

## Formal geofence logic

Given a query point $x=(\phi_1,\lambda_1)$, centre $c=(\phi_2,\lambda_2)$, and Earth-radius constant $R=6{,}371{,}000$ metres, the code computes:

\[
a=\sin^2\left(\frac{\Delta\phi}{2}\right)+\cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right),\qquad d(x,c)=2R\operatorname{atan2}(\sqrt a,\sqrt{1-a}).
\]

For radius $r$, the predicate is:

\[
\operatorname{inside}(x,c,r)=[d(x,c)\leq r].
\]

This is implemented in [libs/geofence/google_maps_geofence.py](libs/geofence/google_maps_geofence.py) and checked by analytical unit cases in [tests/test_geofence_unit.py](tests/test_geofence_unit.py). Read the full [mathematical foundations](docs/MATHEMATICAL_FOUNDATIONS.md) and [complexity analysis](docs/COMPLEXITY_ANALYSIS.md).

## What the repository currently implements

| Component | Implemented behavior | Important limitation |
|---|---|---|
| Haversine geofence | Spherical great-circle distance and a radius comparison | Radius geometry only; no map, road, boundary-buffer, or GPS-uncertainty model |
| API schema | Range validation plus health/readiness/metrics endpoints | No vehicle integration or safety authorization |
| Google geocoding stub | HTTP request with a five-second timeout and conservative false fallback | It returns true when a response contains “Ohio”; this is not deterministic containment logic |
| Supervisor prototype | Mock zero-coordinate breach and speed threshold | Not parallel hardware control, collision prediction, or braking actuation |
| Benchmark tests | In-memory geometry and serialization microbenchmarks | No checked-in numeric results; not vehicle, network, or end-to-end performance |

## Evidence and metrics

The repository’s benchmark tests use pytest-benchmark to generate raw JSON for the in-memory Haversine calculation, the radius predicate, and response serialization. No numeric metric is displayed here because no committed raw result establishes a current value. Run and retain the benchmark artifact before reporting timing:

```bash
pytest tests/benchmarks/test_geofence_benchmark.py --benchmark-only --benchmark-json=benchmarks/latest.json
python scripts/validate_benchmark_json.py benchmarks/latest.json --summary
```

The file [metrics.py](metrics.py) is a synthetic demonstration generator: it uses random latency samples, a sleep-based workload, and hard-coded precision/recall. Its output is not benchmark or safety-validation evidence.

## Research questions

1. What error does the Haversine implementation have relative to an independent geodesic reference over a stated geographic test grid?
2. How do GPS noise, latitude, radius, and boundary buffers affect false allow/deny outcomes in labeled simulated trajectories?
3. What are separate latency distributions for in-memory geometry and the external Google-geocoding path?
4. Which failures are caught by malformed-response, timeout, and provider-error tests?
5. What safety case, fault-injection plan, simulator coverage, and independent review would be required before considering a vehicle-facing use?

The [academic audit](docs/ACADEMIC_AUDIT.md) records the current evidence and the substantial requirements for any future safety-oriented work.

## Local development

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
PYTHONPATH=. pytest tests --ignore=tests/benchmarks
```

Run the focused geometry tests:

```bash
PYTHONPATH=. pytest tests/test_geofence_unit.py -q
```

## Engineering components

The repository includes FastAPI, Prometheus metrics, containers, infrastructure reference assets, and model/simulation experiments. Their presence is not evidence that they are integrated into a production vehicle system. Treat external services, credentials, model weights, infrastructure configuration, and deployment material as development assets requiring independent validation.

## Limitations

- The code has no vehicle, actuator, sensor, controller-area-network, or braking-hardware integration.
- No timing claim can be inferred from Python wall-clock checks or algorithmic complexity.
- No labeled data or experiment reports establish perception, fatigue, collision, drift, or geofence classification quality.
- The geocoding path is external, response-text-dependent, and unsuitable as a safety boundary.
- The prototype has no formal hazard analysis, safety case, requirements traceability, independent verification, or certification evidence.

## License

See [LICENSE](LICENSE).