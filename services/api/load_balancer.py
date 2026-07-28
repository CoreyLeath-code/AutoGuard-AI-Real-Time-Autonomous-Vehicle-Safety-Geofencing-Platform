import random

import requests

INFERENCE_SERVERS = [
    "http://localhost:8001/predict",
    "http://localhost:8002/predict",
    "http://localhost:8003/predict",
]
REQUEST_TIMEOUT_SECONDS = 5


def route_request(payload):
    server = random.choice(INFERENCE_SERVERS)
    response = requests.post(server, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    return response.json()
