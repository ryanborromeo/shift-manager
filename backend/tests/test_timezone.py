from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_settings_timezone_route_removed_get():
    response = client.get("/settings/timezone")
    assert response.status_code == 404


def test_settings_timezone_route_removed_put():
    response = client.put("/settings/timezone", json={"timezone": "Europe/London"})
    assert response.status_code == 404
