#!/usr/bin/env python3
"""Validate pytest-benchmark JSON before publishing it."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

REQUIRED_STAT_FIELDS = ("min", "max", "mean", "median", "stddev", "rounds")


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def validate(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"{path} does not exist")
    if path.stat().st_size == 0:
        raise ValueError(f"{path} is empty")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("pytest-benchmark output must be a JSON object")

    benchmarks = payload.get("benchmarks")
    if not isinstance(benchmarks, list) or not benchmarks:
        raise ValueError(
            "pytest-benchmark output must contain a non-empty benchmarks list"
        )

    for index, benchmark in enumerate(benchmarks, start=1):
        if not isinstance(benchmark, dict):
            raise ValueError(f"benchmark #{index} must be a JSON object")

        name = benchmark.get("name") or benchmark.get("fullname")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"benchmark #{index} is missing a name")

        stats = benchmark.get("stats")
        if not isinstance(stats, dict):
            raise ValueError(f"{name} is missing a stats object")

        for field in REQUIRED_STAT_FIELDS:
            if field not in stats:
                raise ValueError(f"{name} is missing stats.{field}")
            if not _finite_number(stats[field]):
                raise ValueError(f"{name} has non-finite stats.{field}")

        if stats["rounds"] <= 0:
            raise ValueError(f"{name} must have at least one benchmark round")

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to pytest-benchmark JSON")
    parser.add_argument("--summary", action="store_true", help="Emit Markdown summary")
    args = parser.parse_args()

    payload = validate(args.path)
    benchmarks = payload["benchmarks"]

    if args.summary:
        print(f"- File: `{args.path}`")
        print(f"- Benchmarks: {len(benchmarks)}")
        print()
        print("| Benchmark | Mean | Median | Rounds |")
        print("| :--- | ---: | ---: | ---: |")
        for benchmark in benchmarks:
            name = benchmark.get("fullname") or benchmark["name"]
            stats = benchmark["stats"]
            print(
                f"| `{name}` | {stats['mean']:.9f} | "
                f"{stats['median']:.9f} | {int(stats['rounds'])} |"
            )
    else:
        print(f"Validated {len(benchmarks)} benchmark result(s) in {args.path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
