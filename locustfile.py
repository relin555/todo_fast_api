from locust import HttpUser, task, between
import random


class TodoUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/auth/jwt/login",
            data={
                "username": "test@test.com",
                "password": "12345678"
            }
        )

        token = response.json()["access_token"]

        self.client.headers.update({
            "Authorization": f"Bearer {token}"
        })

    @task
    def create_task(self):
        self.client.post(
            "/tasks/",
            json={
                "title": f"Task {random.randint(1, 100000)}",
                "description": "Load test task",
                "status": "new",
                "priority": random.randint(1, 5)
            }
        )

    @task
    def get_tasks(self):
        self.client.get("/tasks/")