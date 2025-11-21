from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.main.list_shifts")
def test_get_shifts_empty(mock_list_shifts):
    mock_list_shifts.return_value = []
    response = client.get("/shifts")
    assert response.status_code == 200
    assert response.json() == []


@patch("app.main.list_shifts")
def test_get_shifts_multiple(mock_list_shifts):
    mock_list_shifts.return_value = [
        {
            "id": 1,
            "worker_id": 1,
            "start": "2024-02-10T09:00:00-05:00",
            "end": "2024-02-10T17:00:00-05:00"
        },
        {
            "id": 2,
            "worker_id": 2,
            "start": "2024-02-11T10:00:00-05:00",
            "end": "2024-02-11T18:00:00-05:00"
        }
    ]
    response = client.get("/shifts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["worker_id"] == 1
    assert data[0]["start"] == "2024-02-10T09:00:00-05:00"
    assert data[0]["end"] == "2024-02-10T17:00:00-05:00"
    assert data[0]["duration_hours"] == 8.0


@patch("app.main.create_shift")
def test_post_shift_valid(mock_create_shift):
    mock_create_shift.return_value = {
        "id": 1,
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    }
    response = client.post("/shifts", json={
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["worker_id"] == 1
    assert data["start"] == "2024-02-10T09:00:00-05:00"
    assert data["end"] == "2024-02-10T17:00:00-05:00"
    assert data["duration_hours"] == 8.0
    mock_create_shift.assert_called_once_with(1, "2024-02-10T09:00:00-05:00", "2024-02-10T17:00:00-05:00")


@patch("app.main.create_shift")
def test_post_shift_nonexistent_worker(mock_create_shift):
    mock_create_shift.side_effect = ValueError("Worker not found")
    response = client.post("/shifts", json={
        "worker_id": 999,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Worker not found"


@patch("app.main.create_shift")
def test_post_shift_overlap(mock_create_shift):
    mock_create_shift.side_effect = ValueError("Shift overlaps with existing shift for this worker")
    response = client.post("/shifts", json={
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Shift overlaps with existing shift for this worker"


def test_post_shift_exceeds_12_hours():
    response = client.post("/shifts", json={
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-11T10:00:00-05:00"
    })
    assert response.status_code == 422
    assert "detail" in response.json()


def test_post_shift_end_before_start():
    response = client.post("/shifts", json={
        "worker_id": 1,
        "start": "2024-02-10T17:00:00-05:00",
        "end": "2024-02-10T09:00:00-05:00"
    })
    assert response.status_code == 422
    assert "detail" in response.json()


def test_post_shift_invalid_datetime_format():
    response = client.post("/shifts", json={
        "worker_id": 1,
        "start": "invalid-datetime",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 422
    assert "detail" in response.json()


@patch("app.main.get_shift")
def test_get_shift_existing(mock_get_shift):
    mock_get_shift.return_value = {
        "id": 1,
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    }
    response = client.get("/shifts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["worker_id"] == 1
    assert data["start"] == "2024-02-10T09:00:00-05:00"
    assert data["end"] == "2024-02-10T17:00:00-05:00"
    assert data["duration_hours"] == 8.0
    mock_get_shift.assert_called_once_with(1)


@patch("app.main.get_shift")
def test_get_shift_nonexistent(mock_get_shift):
    mock_get_shift.return_value = None
    response = client.get("/shifts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shift not found"


@patch("app.main.update_shift")
def test_put_shift_valid(mock_update_shift):
    mock_update_shift.return_value = {
        "id": 1,
        "worker_id": 1,
        "start": "2024-02-10T10:00:00-05:00",
        "end": "2024-02-10T18:00:00-05:00"
    }
    response = client.put("/shifts/1", json={
        "worker_id": 1,
        "start": "2024-02-10T10:00:00-05:00",
        "end": "2024-02-10T18:00:00-05:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["worker_id"] == 1
    assert data["start"] == "2024-02-10T10:00:00-05:00"
    assert data["end"] == "2024-02-10T18:00:00-05:00"
    assert data["duration_hours"] == 8.0
    mock_update_shift.assert_called_once_with(1, 1, "2024-02-10T10:00:00-05:00", "2024-02-10T18:00:00-05:00")


@patch("app.main.update_shift")
def test_put_shift_overlap(mock_update_shift):
    mock_update_shift.side_effect = ValueError("Shift overlaps with existing shift for this worker")
    response = client.put("/shifts/1", json={
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Shift overlaps with existing shift for this worker"


@patch("app.main.update_shift")
def test_put_shift_nonexistent(mock_update_shift):
    mock_update_shift.return_value = None
    response = client.put("/shifts/999", json={
        "worker_id": 1,
        "start": "2024-02-10T09:00:00-05:00",
        "end": "2024-02-10T17:00:00-05:00"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Shift not found"


@patch("app.main.delete_shift")
def test_delete_shift_existing(mock_delete_shift):
    mock_delete_shift.return_value = True
    response = client.delete("/shifts/1")
    assert response.status_code == 204
    assert response.text == ""
    mock_delete_shift.assert_called_once_with(1)


@patch("app.main.delete_shift")
def test_delete_shift_nonexistent(mock_delete_shift):
    mock_delete_shift.return_value = None
    response = client.delete("/shifts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shift not found"


@patch("app.crud.get_timezone_setting")
@patch("app.crud.get_entity_by_id")
def test_timezone_conversion_storage_and_retrieval(mock_get_entity, mock_get_tz):
    from datetime import datetime, timezone
    from app.crud import get_shift
    
    mock_get_tz.return_value = "America/New_York"
    
    mock_entity = MagicMock()
    mock_entity.key.id = 1
    mock_entity.__getitem__ = lambda self, key: {
        "worker_id": 1,
        "start_utc": datetime(2024, 2, 10, 14, 0, 0, tzinfo=timezone.utc),
        "end_utc": datetime(2024, 2, 10, 22, 0, 0, tzinfo=timezone.utc)
    }[key]
    mock_get_entity.return_value = mock_entity
    
    shift = get_shift(1)
    assert shift is not None
    assert shift["start"] == "2024-02-10T09:00:00-05:00"
    assert shift["end"] == "2024-02-10T17:00:00-05:00"


@patch("app.crud.get_timezone_setting")
@patch("app.crud.get_entity_by_id")
def test_timezone_change_affects_retrieval(mock_get_entity, mock_get_tz):
    from datetime import datetime, timezone
    from app.crud import get_shift
    
    mock_entity = MagicMock()
    mock_entity.key.id = 1
    mock_entity.__getitem__ = lambda self, key: {
        "worker_id": 1,
        "start_utc": datetime(2024, 2, 10, 14, 0, 0, tzinfo=timezone.utc),
        "end_utc": datetime(2024, 2, 10, 22, 0, 0, tzinfo=timezone.utc)
    }[key]
    mock_get_entity.return_value = mock_entity
    
    mock_get_tz.return_value = "Europe/London"
    shift = get_shift(1)
    assert shift is not None
    assert shift["start"] == "2024-02-10T14:00:00+00:00"
    assert shift["end"] == "2024-02-10T22:00:00+00:00"


@patch("app.crud.list_entities_by_property")
def test_multiple_shifts_per_day_non_overlapping(mock_list_entities):
    from datetime import datetime, timezone
    from app.crud import check_shift_overlap
    
    mock_shift1 = MagicMock()
    mock_shift1.key.id = 1
    mock_shift1.__getitem__ = lambda self, key: {
        "start_utc": datetime(2024, 2, 10, 14, 0, 0, tzinfo=timezone.utc),
        "end_utc": datetime(2024, 2, 10, 18, 0, 0, tzinfo=timezone.utc)
    }[key]
    
    mock_list_entities.return_value = [mock_shift1]
    
    overlap = check_shift_overlap(
        1,
        datetime(2024, 2, 10, 19, 0, 0, tzinfo=timezone.utc),
        datetime(2024, 2, 10, 23, 0, 0, tzinfo=timezone.utc)
    )
    assert overlap is False


def test_duration_computation_accuracy():
    from app.models import ShiftResponse
    
    shift = ShiftResponse(
        id=1,
        worker_id=1,
        start="2024-02-10T09:00:00-05:00",
        end="2024-02-10T17:00:00-05:00"
    )
    
    assert shift.duration_hours == 8.0
    
    shift_half = ShiftResponse(
        id=2,
        worker_id=1,
        start="2024-02-10T09:00:00-05:00",
        end="2024-02-10T13:30:00-05:00"
    )
    
    assert shift_half.duration_hours == 4.5
