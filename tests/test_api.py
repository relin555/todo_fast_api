from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.auth.users import current_active_user

class FakeUser:
    id = "00000000-0000-0000-0000-000000000001"
    is_active = True
    is_superuser = False
    is_verified = True

async def override_current_user():
    return FakeUser()

app.dependency_overrides[current_active_user] = override_current_user

client = TestClient(app)

def test_create_task_invalid_data():
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task"
        }
    )
    assert response.status_code == 422

# def test_get_not_existing_task():
#     response = client.get("/tasks/999999")
#     assert response.status_code == 404

@pytest.mark.asyncio
async def test_docs():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/docs")
    assert response.status_code == 200
