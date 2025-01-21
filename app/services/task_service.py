from celery_app.celery_config import celery_app
import time
from app.services.sqlite_service import update_task, validate_task
import logging

logger = logging.getLogger(__name__)


@celery_app.task
def example_task(task_id: str = None) -> None:
    """Simulates a long-running task."""
    try:
        # Validate task_id
        validate_task(task_id, "STARTED")
        logger.info(f"Task {task_id} started.")
        update_task(task_id, "STARTED")

        # Simulate work
        time.sleep(5)
        logger.info("Task finished successfully.")

        # Update the task status to SUCCESS
        update_task(task_id, "SUCCESS")
    except ValueError as e:
        logger.error(f"Validation error for task {task_id}: {e}")
        update_task(task_id, "FAILURE")
        raise e
    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {e}")
        update_task(task_id, "FAILURE")
        raise e
