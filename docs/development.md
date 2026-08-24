# Local Development Guide

## Prerequisites

| Tool | Min version | Notes |
|---|---|---|
| Python | 3.10 | 3.11+ also supported |
| Docker + Compose | 24 / v2 | For Kafka & Redis |
| NVIDIA GPU (optional) | CUDA 12 | Models fall back to CPU automatically |
| kubectl + Helm | latest | Only needed for K8s deploys |
| Terraform | 1.7+ | Only needed for infra changes |

## Quick start (local dev)

```bash
# 1. Clone and enter the repo
git clone https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform.git
cd AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install all dependencies
make install                 # or: pip install -r requirements.txt

# 4. Start Kafka + Redis
make infra-up                # or: docker-compose up -d kafka redis

# 5. (Optional) generate a synthetic dataset
make generate-data

# 6. Start the FastAPI backend
make dev-api                 # listens on http://localhost:8000

# 7. Start the gRPC server (separate terminal)
make dev-grpc                # listens on port 50051

# 8. Start the Streamlit dashboard (separate terminal)
make dev-dashboard           # opens at http://localhost:8501

# 9. (Optional) stream simulated sensor data
PYTHONPATH=. python libs/streaming/kafka_producer.py
```

## Running tests

```bash
make test         # pytest tests/
make coverage     # with coverage report
```

## Environment variables

Create a `.env` file at the repo root (never commit it):

```env
GOOGLE_API_KEY=your_key_here
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ACCOUNT=...
```

Load it before running:
```bash
export $(cat .env | xargs)
```

## Component-specific instructions

### services/api

```bash
# Run tests specific to the API
PYTHONPATH=. pytest tests/ -k api

# Access auto-generated OpenAPI docs
open http://localhost:8000/docs
```

### libs/simulation (RL training)

```bash
make train-rl
# or
PYTHONPATH=. python -m libs.simulation.train_rl
```

### libs/risk-engine-cpp

Requires a C++ compiler (g++ 11+):

```bash
cd libs/risk-engine-cpp
g++ -O2 -shared -fPIC -o risk_engine.so risk_engine.cpp
```

## Docker build

```bash
# Build the API image from repo root
docker build -f services/api/Dockerfile -t autoguard-api .

# Or spin up the full stack
docker-compose up --build
```

## Kubernetes deploy (staging / production)

```bash
# Apply HPA
kubectl apply -f infra/k8s/hpa.yaml

# Deploy via Helm (ensure chart exists under infra/helm/autoguard)
helm upgrade --install autoguard ./infra/helm/autoguard
```

## Linting and formatting

```bash
make lint    # flake8
make format  # black
```

## Useful Make targets

```
make help
```
