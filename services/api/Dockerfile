# ── Stage 1: dependency builder ───────────────────────────────────────────────
FROM nvidia/cuda:13.5.0-runtime-ubuntu22.04 AS builder

WORKDIR /build
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM nvidia/cuda:13.5.0-runtime-ubuntu22.04

WORKDIR /app

# Install minimal runtime system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY apps/ apps/
COPY services/ services/
COPY libs/ libs/

# Run as a non-root user
RUN useradd --uid 1000 --create-home appuser
USER appuser

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PYTHONPATH=/app

EXPOSE 8000 50051

# urllib.request is Python stdlib and always available in the container
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')"

CMD ["python3", "-m", "uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
