from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.crud.get_entity")
def test_get_timezone_default(mock_get_entity):
    mock_get_entity.return_value = None
    response = client.get("/settings/timezone")
    assert response.status_code == 200
    assert response.json() == {"timezone": "UTC"}


@patch("app.crud.get_entity")
def test_get_timezone_existing(mock_get_entity):
    mock_entity = MagicMock()
    mock_entity.get.return_value = "America/New_York"
    mock_get_entity.return_value = mock_entity
    
    response = client.get("/settings/timezone")
    assert response.status_code == 200
    assert response.json() == {"timezone": "America/New_York"}


@patch("app.crud.put_entity")
def test_put_timezone_valid(mock_put_entity):
    response = client.put("/settings/timezone", json={"timezone": "Europe/London"})
    assert response.status_code == 200
    assert response.json() == {"timezone": "Europe/London"}
    mock_put_entity.assert_called_once()


def test_put_timezone_invalid():
    response = client.put("/settings/timezone", json={"timezone": "Invalid/Timezone"})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_put_timezone_missing_field():
    response = client.put("/settings/timezone", json={})
    assert response.status_code == 422
    assert "detail" in response.json()


@patch("app.crud.put_entity")
def test_put_timezone_various_valid_timezones(mock_put_entity):
    valid_timezones = ["UTC", "America/New_York", "Asia/Tokyo", "Europe/Paris"]
    for tz in valid_timezones:
        response = client.put("/settings/timezone", json={"timezone": tz})
        assert response.status_code == 200
        assert response.json() == {"timezone": tz}


def test_put_timezone_invalid_formats():
    invalid_timezones = ["GMT+5", "Invalid/Zone", "", "BadZone", "America/InvalidCity"]
    for tz in invalid_timezones:
        response = client.put("/settings/timezone", json={"timezone": tz})
        assert response.status_code == 422, f"Failed for timezone '{tz}': {response.status_code} - {response.json()}"


def test_put_timezone_empty_string():
    response = client.put("/settings/timezone", json={"timezone": ""})
    assert response.status_code == 422


def test_put_timezone_null_value():
    response = client.put("/settings/timezone", json={"timezone": None})
    assert response.status_code == 422


def test_put_timezone_numeric_value():
    response = client.put("/settings/timezone", json={"timezone": 12345})
    assert response.status_code == 422


def test_put_timezone_very_long_string():
    long_string = "A" * 1000
    response = client.put("/settings/timezone", json={"timezone": long_string})
    assert response.status_code == 422


def test_put_timezone_special_characters():
    response = client.put("/settings/timezone", json={"timezone": "America/New_York!@#$"})
    assert response.status_code == 422


@patch("app.crud.put_entity")
def test_put_timezone_case_variations(mock_put_entity):
    response = client.put("/settings/timezone", json={"timezone": "america/new_york"})
    assert response.status_code == 422
