"""Microbenchmarks for AutoGuard's core geofencing calculations.

These tests intentionally avoid network and external-service dependencies so the
scheduled benchmark workflow produces stable, reproducible pytest-benchmark JSON.
"""

from libs.geofence.google_maps_geofence import haversine, is_inside_geofence


VEHICLE_LAT = 37.7749
VEHICLE_LNG = -122.4194
GEOFENCE_LAT = 37.7755
GEOFENCE_LNG = -122.4180
GEOFENCE_RADIUS_METERS = 250.0


def test_haversine_distance_benchmark(benchmark):
    """Measure the latency of the core Haversine distance calculation."""
    distance = benchmark(
        haversine,
        VEHICLE_LAT,
        VEHICLE_LNG,
        GEOFENCE_LAT,
        GEOFENCE_LNG,
    )

    assert distance > 0.0


def test_geofence_membership_benchmark(benchmark):
    """Measure the end-to-end in-memory geofence membership decision."""
    is_inside = benchmark(
        is_inside_geofence,
        VEHICLE_LAT,
        VEHICLE_LNG,
        GEOFENCE_LAT,
        GEOFENCE_LNG,
        GEOFENCE_RADIUS_METERS,
    )

    assert is_inside is True
