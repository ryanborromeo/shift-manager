from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_timezone_returns_default():
    """GET /settings/timezone returns Etc/UTC by default with valid metadata."""
    response = client.get("/settings/timezone")
    assert response.status_code == 200
    data = response.json()
    assert "timezone" in data
    assert "currentLocalTime" in data
    assert "currentUtcOffset" in data
    assert "standardUtcOffset" in data
    assert "hasDayLightSaving" in data
    assert "isDayLightSavingActive" in data


def test_put_timezone_valid():
    """PUT /settings/timezone with valid timezone updates and returns metadata."""
    response = client.put("/settings/timezone", json={"timezone": "Europe/London"})
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "Europe/London"
    assert "currentLocalTime" in data
    assert "currentUtcOffset" in data


def test_put_timezone_invalid():
    """PUT /settings/timezone with invalid timezone returns 400."""
    response = client.put("/settings/timezone", json={"timezone": "Invalid/Zone"})
    assert response.status_code == 400
    assert "Invalid timezone identifier" in response.json()["detail"]


def test_get_timezone_after_update():
    """GET /settings/timezone reflects previously set timezone."""
    client.put("/settings/timezone", json={"timezone": "America/New_York"})
    response = client.get("/settings/timezone")
    assert response.status_code == 200
    assert response.json()["timezone"] == "America/New_York"


def test_list_available_timezones():
    """GET /settings/timezones returns a list of IANA timezone identifiers."""
    response = client.get("/settings/timezones")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Etc/UTC" in data
    assert "America/New_York" in data
