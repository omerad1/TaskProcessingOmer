import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_create_task_success():
    """Test successful creation of a task."""
    with patch("app.routers.tasks.save_task") as mock_save_task, \
            patch("celery_app.celery_config.celery_app.send_task") as mock_send_task:
        mock_save_task.return_value = None
        mock_send_task.return_value = None

        response = client.post("/tasks/")
        assert response.status_code == 201
        assert "task_id" in response.json()
        mock_save_task.assert_called_once()
        mock_send_task.assert_called_once()


def test_get_task_status_success():
    """Test successful retrieval of task status."""
    with patch("app.routers.tasks.get_task", return_value={"task_id": "test-task-id", "status": "PENDING"}):
        response = client.get("/tasks/test-task-id")
        assert response.status_code == 200
        assert response.json() == {"task_id": "test-task-id", "status": "PENDING"}
