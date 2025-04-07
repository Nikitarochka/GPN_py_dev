from locust import HttpUser, task, between

class MeasurementUser(HttpUser):
    host = "http://web:8000"
    wait_time = between(1, 5)

    @task
    def post_measurement(self):
        payload = {
            "device_id": "device1",
            "timestamp": "2025-04-07T12:00:00Z",
            "data": {"x": 1.23, "y": 2.34, "z": 3.45}
        }
        self.client.post("/measurements", json=payload)

    @task
    def get_analysis(self):
        self.client.get("/analysis?device_id=device1")
