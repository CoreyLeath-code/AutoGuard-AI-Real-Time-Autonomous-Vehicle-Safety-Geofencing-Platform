"""Focused core unit tests that replace duplicated smoke coverage."""

import numpy as np

from libs.models.ear_metric import compute_ear
from libs.models.model_registry import ModelRegistry
from libs.pipelines.drift_detection import detect_drift


def test_drift_detection_flags_only_statistically_distinct_samples():
    reference = np.linspace(0.0, 1.0, 100)
    near_match = reference + 0.0001
    shifted = reference + 10.0

    assert not detect_drift(reference, near_match)
    assert detect_drift(reference, shifted)


def test_model_registry_overwrites_versions_and_lists_registered_keys():
    registry = ModelRegistry()
    first = object()
    replacement = object()

    registry.register("v1", first)
    registry.register("v1", replacement)
    registry.register("v2", object())

    assert registry.get("v1") is replacement
    assert registry.get("missing") is None
    assert registry.list_versions() == ["v1", "v2"]


def test_compute_ear_matches_known_geometry():
    eye_points = np.array(
        [
            [0.0, 0.0],
            [1.0, 1.0],
            [2.0, 1.0],
            [4.0, 0.0],
            [2.0, -1.0],
            [1.0, -1.0],
        ]
    )

    assert compute_ear(eye_points) == 0.5
