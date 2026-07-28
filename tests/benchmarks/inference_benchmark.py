import time

import requests

API_URL = "http://localhost:8000/predict"
REQUEST_TIMEOUT_SECONDS = 5

payload = {"speed": 70, "latitude": 37.77, "longitude": -122.41}


def benchmark(n=100):
    start = time.time()
    for _ in range(n):
        requests.post(API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    end = time.time()
    avg_latency = (end - start) / n
    print(f"Average latency: {avg_latency*1000:.2f} ms")


if __name__ == "__main__":
    benchmark()
