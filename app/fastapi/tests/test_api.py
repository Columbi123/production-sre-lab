
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


@pytest.fixture
def sample_task():
    return {
        "id": 1,
        "title": "Check SRE infrastructure",
        "completed": False,
        "created_at": datetime(
            2026, 10, 23, tzinfo=timezone.utc
        ),
    }


def test_root_and_health():
    root = client.get("/")
    health = client.get("/health")

    assert root.status_code == 200
    assert root.json()["version"] == "0.3.0"

    assert health.status_code == 200
    assert health.json()["status"] == "healthy"


def test_ready_success(monkeypatch):
    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: {"result": 1},
    )

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_ready_database_failure(monkeypatch):
    def database_unavailable(*args, **kwargs):
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )

    monkeypatch.setattr(
        main, "run_query", database_unavailable
    )

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Database unavailable"
    )


def test_create_task(monkeypatch, sample_task):
    def fake_query(sql, params=(), fetch=None):
        assert "INSERT INTO tasks" in sql
        assert params == (
            "Check SRE infrastructure", False
        )
        assert fetch == "one"
        return sample_task

    monkeypatch.setattr(main, "run_query", fake_query)

    response = client.post(
        "/tasks",
        json={"title": "Check SRE infrastructure"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["completed"] is False


def test_get_tasks(monkeypatch, sample_task):
    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: [sample_task],
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_task_not_found(monkeypatch):
    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: None,
    )

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(monkeypatch, sample_task):
    updated_task = {
        **sample_task,
        "title": "Infrastructure verified",
        "completed": True,
    }

    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: updated_task,
    )

    response = client.put(
        "/tasks/1",
        json={
            "title": "Infrastructure verified",
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task(monkeypatch):
    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: {"id": 1},
    )

    response = client.delete("/tasks/1")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_nonexistent_task(monkeypatch):
    monkeypatch.setattr(
        main,
        "run_query",
        lambda *args, **kwargs: None,
    )

    response = client.delete("/tasks/999")

    assert response.status_code == 404


def test_empty_title_rejected():
    response = client.post(
        "/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 422
