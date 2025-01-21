import sqlite3
import os
from typing import Optional, Dict
from app.services.util import validate_task

# Define the database file path
DATABASE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "tasks.db"))


def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_done TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_task(task_id: str, status: str):
    """
    Save a new task with PENDING status.
    Raises ValueError if inputs are invalid.
    """
    validate_task(task_id, status)

    print(f"Saving task {task_id} with status {status}")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO tasks (task_id, status)
            VALUES (?, ?)
        """, (task_id, status))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Task with task_id '{task_id}' already exists.") from e
    finally:
        conn.close()


def update_task(task_id: str, status: str):
    """
    Update the status and result of a task.
    Raises ValueError if inputs are invalid or if the task is not found.
    """
    validate_task(task_id, status)
    print(f"Updating task {task_id} to status {status}")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?, date_done = CURRENT_TIMESTAMP
        WHERE task_id = ?
    """, (status, task_id))

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError(f"Task with task_id '{task_id}' not found.")
    conn.commit()
    conn.close()


def get_task(task_id: str) -> Optional[Dict[str, str]]:
    """
    Retrieve a task's status.
    Returns a dictionary with task_id and status if found, or None if not found.
    Raises ValueError if task_id is invalid.
    """
    if not task_id or not isinstance(task_id, str):
        raise ValueError("Invalid task_id. Must be a non-empty string.")

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status FROM tasks WHERE task_id = ?
    """, (task_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"task_id": task_id, "status": result[0]}
    return None
