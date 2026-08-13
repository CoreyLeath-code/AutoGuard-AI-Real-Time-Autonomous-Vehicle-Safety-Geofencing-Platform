# Verification Scope

This repository uses verification-first rules for safety-oriented claims. Tests and documentation must describe existing behavior rather than create new vehicle-control capabilities merely to satisfy an audit.

## Stop condition

Do not create braking-distance, polygon-geofence, boundary-crossing, or alert/notification implementations merely so requested verification tests have something to test. If the corresponding implementation does not already exist, record it as `NOT IMPLEMENTED` and do not reinterpret another component as equivalent.

In particular, the existing Haversine radius predicate is not a polygon geofence. Supervisor state flags are not an alert/notification subsystem. Mock braking-force fields are not a stopping-distance physics model or braking actuator integration.

## Current orientation

- Radius geofence geometry: `libs/geofence/google_maps_geofence.py`
- Radius geofence tests: `tests/test_geofence_unit.py`
- Prototype supervisor rules: `agents/supervisor.py`
- Braking/stopping-distance physics model: `NOT IMPLEMENTED`
- Polygon point-in-polygon boundary model: `NOT IMPLEMENTED`
- Boundary-crossing alert/notification subsystem: `NOT IMPLEMENTED`

Future pull requests should preserve these distinctions unless runnable code and tests actually implement the missing behavior. Performance, safety, latency, or capability claims require evidence produced by the same change and must identify the command and commit used to produce that evidence.
