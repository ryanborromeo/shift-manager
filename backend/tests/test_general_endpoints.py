from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_unsupported_method_workers():
    response = client.patch("/workers/1")
    assert response.status_code == 405


def test_unsupported_method_shifts():
    response = client.patch("/shifts/1")
    assert response.status_code == 405

def test_invalid_content_type():
    response = client.post(
        "/workers",
        content=b"name=John",
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code in [422, 400]


def test_malformed_json_workers():
    response = client.post(
        "/workers",
        content=b"{invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_malformed_json_shifts():
    response = client.post(
        "/shifts",
        content=b"{worker_id: 1, start:",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
