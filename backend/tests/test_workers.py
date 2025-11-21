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


@patch("app.main.get_worker")
def test_get_worker_negative_id(mock_get_worker):
    mock_get_worker.return_value = None
    response = client.get("/workers/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Worker not found"


@patch("app.main.get_worker")
def test_get_worker_zero_id(mock_get_worker):
    mock_get_worker.return_value = None
    response = client.get("/workers/0")
    assert response.status_code == 404
    assert response.json()["detail"] == "Worker not found"


@patch("app.main.get_worker")
def test_get_worker_very_large_id(mock_get_worker):
    mock_get_worker.return_value = None
    response = client.get("/workers/9999999999999999999")
    assert response.status_code == 404


def test_get_worker_non_integer_id():
    response = client.get("/workers/abc")
    assert response.status_code == 422


@patch("app.main.create_worker")
def test_post_worker_special_characters(mock_create_worker):
    mock_create_worker.return_value = {"id": 1, "name": "John O'Brien & Co."}
    response = client.post("/workers", json={"name": "John O'Brien & Co."})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "John O'Brien & Co."}


@patch("app.main.create_worker")
def test_post_worker_unicode_characters(mock_create_worker):
    mock_create_worker.return_value = {"id": 1, "name": "José García 李明"}
    response = client.post("/workers", json={"name": "José García 李明"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "José García 李明"}


@patch("app.main.create_worker")
def test_post_worker_extremely_long_name(mock_create_worker):
    long_name = "A" * 1001
    mock_create_worker.return_value = {"id": 1, "name": long_name}
    response = client.post("/workers", json={"name": long_name})
    assert response.status_code == 201
    assert response.json()["name"] == long_name


def test_post_worker_null_value():
    response = client.post("/workers", json={"name": None})
    assert response.status_code == 422


def test_post_worker_numeric_name():
    response = client.post("/workers", json={"name": 12345})
    assert response.status_code == 422


@patch("app.main.update_worker")
def test_put_worker_negative_id(mock_update_worker):
    mock_update_worker.return_value = None
    response = client.put("/workers/-1", json={"name": "John Doe"})
    assert response.status_code == 404


@patch("app.main.delete_worker")
def test_delete_worker_negative_id(mock_delete_worker):
    mock_delete_worker.return_value = None
    response = client.delete("/workers/-1")
    assert response.status_code == 404
