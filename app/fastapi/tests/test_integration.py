import os
import uuid
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from main import app


pytestmark = pytest.mark.integration

client = TestClient(app)


def connect_db():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )


@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "db"
        / "schema.sql"
    )

    with connect_db() as conn:
        conn.execute(
            schema_path.read_text(encoding="utf-8")
        )


def test_crud_with_real_postgresql():
    title = f"CI integration {uuid.uuid4().hex[:12]}"
    task_id = None

    try:
        # READINESS
        response = client.get("/ready")
        assert response.status_code == 200

        # CREATE
        response = client.post(
            "/tasks",
            json={"title": title}
        )

        assert response.status_code == 201

        task = response.json()
        task_id = task["id"]

        assert task["title"] == title
        assert task["completed"] is False

        # VERIFY REAL DATABASE WRITE
        with connect_db() as conn:
            row = conn.execute(
                """
                SELECT title, completed
                FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            ).fetchone()

        assert row == (title, False)

        # READ
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 200
        assert response.json()["title"] == title

        # LIST
        response = client.get("/tasks")

        assert response.status_code == 200
        assert any(
            item["id"] == task_id
            for item in response.json()
        )

        # UPDATE
        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "CI integration verified",
                "completed": True
            }
        )

        assert response.status_code == 200
        assert response.json()["completed"] is True

        # DELETE
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 204

        # VERIFY DELETION
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 404

    finally:
        # Remove test data if an assertion failed
        if task_id is not None:
            with connect_db() as conn:
                conn.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,)
                )
