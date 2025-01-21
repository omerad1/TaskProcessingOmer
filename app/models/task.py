from pydantic import BaseModel


class TaskStatus(BaseModel):
    """
    TaskStatus represents the structure of a task's status data.

    Attributes:
        task_id (str): A unique identifier for the task.
        status (str): The current status of the task (e.g., PENDING, SUCCESS).
    """
    task_id: str  # unique identifier
    status: str  # current status of the task
