import os
from datetime import datetime

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="Production SRE Lab API",
    description="Application for SRE infrastructure practice",
    version="0.3.0"
)


# ---------- DATABASE ----------

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
    )


def run_query(query, params=(), fetch=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)

                if fetch == "one":
                    return cursor.fetchone()

                if fetch == "all":
                    return cursor.fetchall()

    except psycopg.OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        ) from exc

    except psycopg.Error as exc:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        ) from exc


# ---------- DATA MODELS ----------

class TaskTitle(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty")

        return value


class TaskCreate(TaskTitle):
    completed: bool = False


class TaskUpdate(TaskTitle):
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime


# ---------- HEALTH CHECKS ----------

@app.get("/")
def root():
    return {
        "message": "Welcome to Production SRE Lab",
        "status": "running",
        "version": "0.3.0",
	"deployment": "ansible"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "sre-api"
    }


@app.get("/ready")
def ready():
    run_query("SELECT 1", fetch="one")

    return {
        "status": "ready",
        "database": "ok"
    }


# ---------- CREATE ----------

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):
    return run_query(
        """
        INSERT INTO tasks (title, completed)
        VALUES (%s, %s)
        RETURNING id, title, completed, created_at
        """,
        (task.title, task.completed),
        fetch="one"
    )


# ---------- READ ----------

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return run_query(
        """
        SELECT id, title, completed, created_at
        FROM tasks
        ORDER BY id
        """,
        fetch="all"
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = run_query(
        """
        SELECT id, title, completed, created_at
        FROM tasks
        WHERE id = %s
        """,
        (task_id,),
        fetch="one"
    )

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


# ---------- UPDATE ----------

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    updated = run_query(
        """
        UPDATE tasks
        SET title = %s, completed = %s
        WHERE id = %s
        RETURNING id, title, completed, created_at
        """,
        (task.title, task.completed, task_id),
        fetch="one"
    )

    if updated is None:
        raise HTTPException(404, "Task not found")

    return updated


# ---------- DELETE ----------

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):
    deleted = run_query(
        "DELETE FROM tasks WHERE id = %s RETURNING id",
        (task_id,),
        fetch="one"
    )

    if deleted is None:
        raise HTTPException(404, "Task not found")

    return Response(status_code=204)
