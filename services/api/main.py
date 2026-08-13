import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel, Field

from .config import settings
from .geofence import check_geofence
from .middleware import (
    GlobalExceptionMiddleware,
    RequestLoggingMiddleware,
    configure_logging,
)
from libs.monitoring.prometheus_metrics import (
    REQUEST_COUNT as request_counter,
    INFERENCE_LATENCY,
)

configure_logging(settings.log_level)

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Expose readiness only while this process is accepting application traffic."""
    application.state.accepting_traffic = True
    try:
        yield
    finally:
        application.state.accepting_traffic = False


app = FastAPI(
    title="AutoGuard AI",
    description="Geofence prototype and telemetry API",
    version="0.1.0",
    lifespan=lifespan,
)
# Keep import-time and test-client behavior deterministic when lifespan is not entered.
app.state.accepting_traffic = True

# Register middleware (outermost first)
app.add_middleware(GlobalExceptionMiddleware)
app.add_middleware(RequestLoggingMiddleware)

_START_TIME = time.time()


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class TelemetryRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Vehicle latitude")
    lon: float = Field(..., ge=-180, le=180, description="Vehicle longitude")
    speed: float = Field(0.0, ge=0, description="Vehicle speed in m/s")
    vehicle_id: str = Field(..., min_length=1, description="Unique vehicle identifier")


class PredictionResponse(BaseModel):
    vehicle_id: str
    geofence_valid: bool
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float


# ---------------------------------------------------------------------------
# Health endpoints (used by Kubernetes liveness / readiness / startup probes)
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["health"])
@app.get("/health/live", response_model=HealthResponse, tags=["health"])
async def liveness():
    """Kubernetes liveness probe – confirms the process is alive."""
    return HealthResponse(
        status="alive",
        uptime_seconds=round(time.time() - _START_TIME, 2),
    )


@app.get("/health/ready", response_model=HealthResponse, tags=["health"])
async def readiness():
    """Report whether this process should receive application traffic."""
    if not app.state.accepting_traffic:
        return PlainTextResponse(
            "draining",
            status_code=503,
            headers={"Retry-After": "5"},
        )
    return HealthResponse(
        status="ready",
        uptime_seconds=round(time.time() - _START_TIME, 2),
    )


# ---------------------------------------------------------------------------
# Prometheus metrics scrape endpoint
# ---------------------------------------------------------------------------

@app.get("/metrics", response_class=PlainTextResponse, tags=["observability"])
async def metrics():
    """Expose Prometheus metrics for scraping by a Prometheus server."""
    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


# ---------------------------------------------------------------------------
# Inference endpoint
# ---------------------------------------------------------------------------

@app.post("/predict", response_model=PredictionResponse, tags=["inference"])
async def predict(body: TelemetryRequest):
    """Validate vehicle telemetry against the active geofence and run inference.

    The geofence check is I/O-bound (external HTTP call) and is offloaded to a
    thread-pool executor so the async event loop is never blocked.
    """
    start_time = time.perf_counter()
    request_counter.inc()
    try:
        geofence_valid = await asyncio.to_thread(check_geofence, body.lat, body.lon)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Geofence check failed: {exc}") from exc
    latency_s = time.perf_counter() - start_time
    INFERENCE_LATENCY.observe(latency_s)
    latency_ms = round(latency_s * 1000, 3)
    return PredictionResponse(
        vehicle_id=body.vehicle_id,
        geofence_valid=geofence_valid,
        latency_ms=latency_ms,
    )
