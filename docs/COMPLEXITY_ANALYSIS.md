# Complexity Analysis

## Variables

- $N$: number of independent in-memory geofence membership queries
- $L$: character size of an external geocoding response
- $B$: number of pytest-benchmark rounds

This analysis is derived from the checked-in code and does not establish deadline, capacity, or vehicle-safety behavior.

## Operations

| Operation | Best | Average | Worst | Auxiliary space |
|---|---:|---:|---:|---:|
| One Haversine distance | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| One radius membership decision | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| $N$ independent radius checks | $O(N)$ | $O(N)$ | $O(N)$ | $O(1)$ beyond outputs |
| External geocoding stub | network-bound | network-bound | bounded by 5 s timeout or failure | $O(L)$ response object |
| Supervisor prototype frame | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ plus trace entries |

The Haversine function evaluates a fixed number of trigonometric operations, so its algorithmic cost is constant per query. In practice, numerical-library, Python interpreter, and hardware effects determine observed timing.

The external API route is not comparable with the in-memory Haversine predicate: its latency depends on DNS, TLS, provider service, response size, and thread-pool scheduling. Any future performance report must separate those operations and include raw timing artifacts.

## Benchmark interpretation

The repository's pytest-benchmark tests cover in-memory Haversine, radius membership, and Pydantic response serialization. They do not benchmark vehicle I/O, perception, collision avoidance, physical actuation, external geocoding, load, or end-to-end safety behavior. Asymptotic complexity never establishes a real-time deadline.
