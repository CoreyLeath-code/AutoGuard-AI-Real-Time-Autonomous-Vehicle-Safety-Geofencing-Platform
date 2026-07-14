window.BENCHMARK_DATA = {
  "lastUpdate": 1783997356919,
  "repoUrl": "https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "name": "Corey Leath",
            "username": "CoreyLeath-code",
            "email": "corey22blue@hotmail.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "b492e240744345555cb910f6ab34199286025303",
          "message": "Update daily_benchmarks.yml",
          "timestamp": "2026-07-13T03:43:48Z",
          "url": "https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform/commit/b492e240744345555cb910f6ab34199286025303"
        },
        "date": 1783997356525,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_geofence_benchmark.py::test_haversine_distance_benchmark",
            "value": 1321323.2537897623,
            "unit": "iter/sec",
            "range": "stddev: 2.8140210125750597e-7",
            "extra": "mean: 756.817074952585 nsec\nrounds: 60369"
          },
          {
            "name": "tests/benchmarks/test_geofence_benchmark.py::test_geofence_membership_benchmark",
            "value": 1126074.9268530246,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016477300200094728",
            "extra": "mean: 888.0403747152432 nsec\nrounds: 183184"
          },
          {
            "name": "tests/benchmarks/test_geofence_benchmark.py::test_prediction_response_serialization_benchmark",
            "value": 392450.31959979783,
            "unit": "iter/sec",
            "range": "stddev: 6.571493918420662e-7",
            "extra": "mean: 2.5480932236716036 usec\nrounds: 20660"
          }
        ]
      }
    ]
  }
}