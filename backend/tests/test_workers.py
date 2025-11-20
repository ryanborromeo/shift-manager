from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.main.list_workers")
def test_get_workers_empty(mock_list_workers):
    mock_list_workers.return_value = []
    response = client.get("/workers")
    assert response.status_code == 200
    assert response.json() == []


@patch("app.main.list_workers")
def test_get_workers_multiple(mock_list_workers):
    mock_list_workers.return_value = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]
    response = client.get("/workers")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]


@patch("app.main.create_worker")
def test_post_worker_valid(mock_create_worker):
    mock_create_worker.return_value = {"id": 1, "name": "Alice Johnson"}
    response = client.post("/workers", json={"name": "Alice Johnson"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Alice Johnson"}
    mock_create_worker.assert_called_once_with("Alice Johnson")


def test_post_worker_empty_name():
    response = client.post("/workers", json={"name": ""})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_post_worker_whitespace_only():
    response = client.post("/workers", json={"name": "   "})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_post_worker_missing_name():
    response = client.post("/workers", json={})
    assert response.status_code == 422
    assert "detail" in response.json()


@patch("app.main.get_worker")
def test_get_worker_existing(mock_get_worker):
    mock_get_worker.return_value = {"id": 1, "name": "John Doe"}
    response = client.get("/workers/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe"}
    mock_get_worker.assert_called_once_with(1)


@patch("app.main.get_worker")
def test_get_worker_nonexistent(mock_get_worker):
    mock_get_worker.return_value = None
    response = client.get("/workers/999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Worker not found"


@patch("app.main.update_worker")
def test_put_worker_valid(mock_update_worker):
    mock_update_worker.return_value = {"id": 1, "name": "Robert Brown"}
    response = client.put("/workers/1", json={"name": "Robert Brown"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Robert Brown"}
    mock_update_worker.assert_called_once_with(1, "Robert Brown")


def test_put_worker_empty_name():
    response = client.put("/workers/1", json={"name": ""})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_put_worker_whitespace_only():
    response = client.put("/workers/1", json={"name": "   "})
    assert response.status_code == 422
    assert "detail" in response.json()


@patch("app.main.update_worker")
def test_put_worker_nonexistent(mock_update_worker):
    mock_update_worker.return_value = None
    response = client.put("/workers/999", json={"name": "Robert Brown"})
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Worker not found"


@patch("app.main.delete_worker")
def test_delete_worker_existing(mock_delete_worker):
    mock_delete_worker.return_value = True
    response = client.delete("/workers/1")
    assert response.status_code == 204
    assert response.text == ""
    mock_delete_worker.assert_called_once_with(1)


@patch("app.main.delete_worker")
def test_delete_worker_nonexistent(mock_delete_worker):
    mock_delete_worker.return_value = None
    response = client.delete("/workers/999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Worker not found"
