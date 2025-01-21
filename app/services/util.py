def validate_task(task_id: str, status: str) -> None:
    """
    Validate the task ID and status.
    Raises:
        ValueError: If task_id or status is invalid.
    """
    if not task_id or not isinstance(task_id, str):
        raise ValueError("Invalid task_id. Must be a non-empty string.")
    if status not in {"PENDING", "STARTED", "SUCCESS", "FAILURE"}:
        raise ValueError("Invalid status. Must be one of PENDING, STARTED, SUCCESS, FAILURE.")