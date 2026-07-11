from locust import HttpUser, task, between


class AutoGuardUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        self.client.post(
            "/predict", json={"speed": 65, "latitude": 37.77, "longitude": -122.41}
        )
