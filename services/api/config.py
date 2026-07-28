"""Centralised application settings.

All configuration is read from environment variables (or a .env file when
running locally).  No secrets are hard-coded here; see .env.example for the
full list of supported variables.
"""

import os


class Settings:
    """Application settings resolved from environment variables at import time."""

    # FastAPI — bind to all interfaces by default so the service is reachable
    # inside Docker / Kubernetes pods; override with 127.0.0.1 for localhost-only.
    api_host: str = os.environ.get("API_HOST", "0.0.0.0")  # nosec B104
    api_port: int = int(os.environ.get("API_PORT", "8000"))
    log_level: str = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Geofencing
    google_api_key: str = os.environ.get("GOOGLE_API_KEY", "")
    geofence_center_lat: float = float(os.environ.get("GEOFENCE_CENTER_LAT", "40.0"))
    geofence_center_lon: float = float(os.environ.get("GEOFENCE_CENTER_LON", "-83.0"))
    geofence_radius_m: float = float(os.environ.get("GEOFENCE_RADIUS_M", "50000.0"))

    # Redis
    redis_host: str = os.environ.get("REDIS_HOST", "localhost")
    redis_port: int = int(os.environ.get("REDIS_PORT", "6379"))

    # Kafka
    kafka_bootstrap_servers: str = os.environ.get(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )

    # OpenTelemetry
    otel_endpoint: str = os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
    )
    otel_service_name: str = os.environ.get("OTEL_SERVICE_NAME", "autoguard-api")


settings = Settings()
