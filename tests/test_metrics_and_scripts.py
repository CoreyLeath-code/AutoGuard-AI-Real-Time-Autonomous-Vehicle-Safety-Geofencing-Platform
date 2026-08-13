"""Tests for benchmark helpers and repository utility scripts."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from metrics import AutoGuardBenchmarker
from scripts import generate_data, generate_metrics_table
from scripts.validate_benchmark_json import main, validate


def test_autoguard_benchmarker_generates_and_saves_metrics(monkeypatch, tmp_path):
    times = iter([100.0, 102.0])
    monkeypatch.setattr("metrics.time.time", lambda: next(times))
    monkeypatch.setattr("metrics.time.sleep", lambda seconds: None)

    benchmarker = AutoGuardBenchmarker(num_vehicles=2, points_per_vehicle=3)
    metrics = benchmarker.run_benchmark()

    assert metrics.total_vehicles_simulated == 2
    assert metrics.total_telemetry_points == 6
    assert metrics.avg_throughput_eps == 3.0
    assert metrics.geofence_breach_recall == 0.999

    output_path = tmp_path / "metrics_report.json"
    benchmarker.save_metrics_report(metrics, output_path=str(output_path))

    saved = json.loads(output_path.read_text())
    assert saved["total_telemetry_points"] == 6
    assert saved["avg_throughput_eps"] == 3.0


def test_generate_dataset_writes_expected_columns(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    generate_data.generate_dataset(size=5)

    output = tmp_path / "synthetic_vehicle_data.csv"
    assert output.exists()

    frame = pd.read_csv(output)
    assert list(frame.columns) == [
        "speed",
        "latitude",
        "longitude",
        "eye_aspect_ratio",
        "collision_risk",
    ]
    assert len(frame) == 5


def test_generate_inventory_table_outputs_descriptive_markers(capsys):
    print(generate_metrics_table.calculate_project_inventory())
    output = capsys.readouterr().out

    assert "## Repository inventory" in output
    assert "| Inventory item | Value |" in output
    assert "Selected text files" in output
    assert "performance, safety, accuracy, or quality metric" in output


def test_validate_benchmark_json_accepts_pytest_benchmark_shape(tmp_path):
    payload = {
        "benchmarks": [
            {
                "name": "test_latency",
                "stats": {
                    "min": 1.0,
                    "max": 2.0,
                    "mean": 1.5,
                    "median": 1.5,
                    "stddev": 0.1,
                    "rounds": 3,
                },
            }
        ]
    }
    path = tmp_path / "output.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert validate(path) == payload


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({}, "benchmarks list"),
        ({"benchmarks": []}, "benchmarks list"),
        ([], "JSON object"),
        ({"benchmarks": [None]}, "JSON object"),
        ({"benchmarks": [{"stats": {}}]}, "missing a name"),
        ({"benchmarks": [{"name": "x"}]}, "stats object"),
        ({"benchmarks": [{"name": "x", "stats": {"rounds": 0}}]}, "stats.min"),
        (
            {
                "benchmarks": [
                    {
                        "name": "x",
                        "stats": {
                            "min": float("nan"),
                            "max": 1.0,
                            "mean": 1.0,
                            "median": 1.0,
                            "stddev": 0.0,
                            "rounds": 1,
                        },
                    }
                ]
            },
            "non-finite",
        ),
    ],
)
def test_validate_benchmark_json_rejects_invalid_payloads(tmp_path, payload, message):
    path = tmp_path / "output.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        validate(path)


def test_validate_benchmark_json_rejects_missing_empty_and_malformed_files(tmp_path):
    missing = tmp_path / "missing.json"
    with pytest.raises(ValueError, match="does not exist"):
        validate(missing)

    empty = tmp_path / "empty.json"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        validate(empty)

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        validate(malformed)


def test_validate_benchmark_json_summary_cli_outputs_markdown(
    tmp_path, monkeypatch, capsys
):
    payload = {
        "benchmarks": [
            {
                "fullname": "tests/test_perf.py::test_latency",
                "stats": {
                    "min": 1.0,
                    "max": 2.0,
                    "mean": 1.5,
                    "median": 1.5,
                    "stddev": 0.1,
                    "rounds": 3,
                },
            }
        ]
    }
    path = tmp_path / "output.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv", ["validate_benchmark_json.py", str(path), "--summary"]
    )

    assert main() == 0
    output = capsys.readouterr().out
    assert "| Benchmark | Mean | Median | Rounds |" in output
    assert "tests/test_perf.py::test_latency" in output
