# Academic Audit: AutoGuard-AI

## Safety scope

This repository is a software prototype and simulation-oriented collection of geofencing, API, telemetry, and model-support code. It is **not** evidence of a deployable autonomous-vehicle safety system. Nothing in this repository has been shown to control braking hardware, satisfy real-time guarantees, meet a safety standard, or be validated on a vehicle.

A claim is **DERIVED** when it follows from code, **OBSERVED** when it describes the repository, and **NOT MEASURED** when no valid experiment supports it.

## Evidence currently present

| Dimension | Assessment | Evidence |
|---|---|---|
| Direct geometry | **DERIVED** | `libs/geofence/google_maps_geofence.py` implements Haversine great-circle distance and radius membership. |
| Geometry tests | **OBSERVED** | `tests/test_geofence_unit.py` checks zero distance, symmetry, approximate geographic distances, and radius membership. |
| API validation | **OBSERVED** | `services/api/main.py` bounds latitude, longitude, speed, and vehicle-id fields and exposes liveness/readiness/metrics endpoints. |
| Local timeout policy | **OBSERVED** | `agents/guards.py` raises an exception above a configurable Python elapsed-time threshold; it is not hardware monitoring. |
| Benchmark method | **OBSERVED** | `tests/benchmarks/test_geofence_benchmark.py` measures in-memory Haversine/membership and response serialization with pytest-benchmark. |
| Vehicle safety efficacy | **NOT MEASURED** | No vehicle, simulator scenario suite, sensor dataset, independent oracle, ISO 26262/SOTIF process, fault-injection study, or hazard analysis is committed. |
| Latency, throughput, precision, recall | **NOT MEASURED** | README figures have no committed raw artifact. `metrics.py` explicitly generates random simulated latencies and hard-coded precision/recall. |

## Major strengths

1. The Haversine radius predicate is small, inspectable, and supported by basic analytical tests.
2. Request schemas enforce geographic coordinate ranges before the API performs the geofence call.
3. The in-memory benchmark avoids network dependencies and can produce raw pytest-benchmark output.
4. The API records request count and observed handler latency for operational inspection.

## Critical weaknesses and threats to validity

| Gap | Consequence |
|---|---|
| `check_geofence()` calls an external geocoding API and accepts a location when the string “Ohio” appears in a response | It is not a geometric safety boundary, has external latency/failure modes, and cannot substantiate a deterministic geofence claim. |
| Supervisor's “geofence breach” is triggered by latitude or longitude equal to zero | This is explicitly mock behavior, not a geographic containment algorithm. |
| Supervisor measures elapsed wall-clock time in CPython and catches a local exception | This neither enforces a hard real-time deadline nor interacts with a physical circuit breaker. |
| README claims braking, hard real time, latency caps, throughput, and safety performance | These claims are unsupported and must not be made. |
| `metrics.py` uses random samples, `sleep`, and hard-coded precision/recall | Its output is synthetic demonstration data, not a benchmark or validation artifact. |
| No costed trajectory, obstacle, perception, fatigue, or collision-risk validation | Model files alone do not demonstrate safety performance. |

## Research questions for a responsible prototype

1. For known spherical-radius cases, what is the numerical error of the Haversine implementation relative to an independent geodesic reference?
2. How does boundary-classification error vary by latitude, radius, and distance from a radial boundary?
3. What are the latency distributions of the in-memory predicate and the external API path when measured separately?
4. Under simulated, labeled trajectories, how do false allow/deny rates change with GPS noise and boundary buffers?
5. Which failure modes are detected through API timeout, provider-error, and malformed-response tests?

## Claims policy

Use “prototype,” “in-memory geometry benchmark,” “Haversine radius predicate,” and “simulation/research only.” Do not use “autonomous vehicle safety,” “hard real time,” “hardware override,” “braking,” “safety validated,” “precision,” “recall,” “SLA,” or throughput values unless a corresponding, reproducible safety case and valid artifact exist.
