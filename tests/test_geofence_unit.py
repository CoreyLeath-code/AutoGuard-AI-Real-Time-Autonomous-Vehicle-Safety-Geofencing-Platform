"""Unit tests for geofence utility functions in libs/geofence/."""

import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from libs.geofence.google_maps_geofence import (
    haversine,
    is_inside_geofence,
    expand_geofence,
)

# ---------------------------------------------------------------------------
# haversine distance
# ---------------------------------------------------------------------------


def test_haversine_same_point_is_zero():
    assert haversine(0.0, 0.0, 0.0, 0.0) == 0.0


def test_haversine_known_distance_london_paris():
    """London â†’ Paris is approximately 340 km."""
    d = haversine(51.5, -0.12, 48.85, 2.35)
    assert 300_000 < d < 400_000


def test_haversine_symmetry():
    """Distance Aâ†’B must equal distance Bâ†’A."""
    d1 = haversine(40.0, -74.0, 51.5, -0.12)
    d2 = haversine(51.5, -0.12, 40.0, -74.0)
    assert math.isclose(d1, d2, rel_tol=1e-9)


def test_haversine_non_negative():
    """Distance is always non-negative."""
    assert haversine(-33.87, 151.21, 35.68, 139.69) >= 0


def test_haversine_equator_longitude_diff():
    """One degree of longitude on the equator â‰ˆ 111 km."""
    d = haversine(0.0, 0.0, 0.0, 1.0)
    assert 110_000 < d < 113_000


# ---------------------------------------------------------------------------
# is_inside_geofence
# ---------------------------------------------------------------------------


def test_inside_at_center():
    """A point at the exact center must be inside any positive radius."""
    assert is_inside_geofence(37.7749, -122.4194, 37.7749, -122.4194, 1)


def test_outside_far_away():
    """Origin is far outside a San Francisco geofence of 5 km."""
    assert not is_inside_geofence(0.0, 0.0, 37.7749, -122.4194, 5_000)


def test_inside_within_radius():
    """A point 100 m away must be inside a 1 km radius geofence."""
    # Roughly 0.001 degree latitude â‰ˆ 111 m
    assert is_inside_geofence(37.7759, -122.4194, 37.7749, -122.4194, 1_000)


def test_outside_beyond_radius():
    """A point 10 km away must be outside a 1 km radius geofence."""
    assert not is_inside_geofence(37.8650, -122.4194, 37.7749, -122.4194, 1_000)


def test_boundary_exactly_on_edge():
    """A point at exactly the radius distance is inside (<=)."""
    center_lat, center_lon = 40.0, -83.0
    radius = 5_000  # 5 km
    # haversine between center and itself is 0, so always inside
    assert is_inside_geofence(center_lat, center_lon, center_lat, center_lon, radius)


# ---------------------------------------------------------------------------
# expand_geofence
# ---------------------------------------------------------------------------


def test_expand_geofence_increases_radius():
    """Expanded radius must be strictly greater than the original."""
    r = 10_000
    expanded = expand_geofence(40.0, -83.0, r)
    assert expanded > r


def test_expand_geofence_positive_result():
    """Result must always be positive."""
    assert expand_geofence(0.0, 0.0, 500) > 0


# ---------------------------------------------------------------------------
# services/api/geofence: check_geofence falls back gracefully with no API key
# ---------------------------------------------------------------------------


def test_check_geofence_no_key_returns_false(monkeypatch):
    """Without a GOOGLE_API_KEY the check must return False without raising."""
    import services.api.geofence as gf

    monkeypatch.setattr(gf, "GOOGLE_API_KEY", "")
    result = gf.check_geofence(40.0, -83.0)
    assert result is False
