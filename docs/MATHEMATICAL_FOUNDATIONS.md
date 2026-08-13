# Mathematical Foundations

## Scope and safety boundary

This document specifies the implemented Haversine radius check in `libs/geofence/google_maps_geofence.py`. It is a convenience geospatial predicate for prototype work. It is not a vehicle-control or certified safety algorithm.

## Great-circle distance

For two positions with latitude/longitude $(\phi_1,\lambda_1)$ and $(\phi_2,\lambda_2)$ in radians, the code uses Earth radius $R=6{,}371{,}000$ metres and computes

\[
a=\sin^2\left(\frac{\Delta\phi}{2}\right)+\cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right),
\qquad
d=2R\operatorname{atan2}(\sqrt{a},\sqrt{1-a}).
\]

This maps directly to `haversine()`. Unit tests check $d=0$ for equal points, symmetry, and broad known-distance bounds.

## Radius-membership decision

Given a fixed centre $c$, query point $x$, and radius $r$ in metres, the direct predicate is

\[
\operatorname{inside}(x,c,r)=[d(x,c)\leq r].
\]

The boundary is inclusive. `expand_geofence()` returns $1.2r$, but this 1.2 multiplier is marked as placeholder logic and has no traffic model or calibration.

## API geofence behavior is distinct

`services/api/geofence.py` is not an implementation of the mathematical radius predicate. It calls Google geocoding, returns false for absent credentials/errors/no results, and returns true if any response string contains “Ohio.” Treat that as a prototype integration stub with an external five-second request timeout—not as a safe or deterministic geofence.

## Prototype supervisor rule

`agents/supervisor.py` has separate mock rules: it marks a breach if latitude or longitude is exactly zero, and then marks collision risk if that breach coincides with speed above 25 mph. These conditions are source-visible demonstration rules, not physical or geometric collision models. The local five-millisecond threshold is a Python elapsed-time policy that raises and catches `TelemetryDeadlineException`; it does not command a brake or enforce a hard real-time bound.
