import uuid
from app.services.util import validate_task
from fastapi import APIRouter, HTTPException
from celery_app.celery_config import celery_app
from app.services.sqlite_service import save_task, get_task
import redis.asyncio as redis

router = APIRouter(prefix="/tasks", tags=["Tasks"])
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


@router.post("/", status_code=201)
async def create_task():
    """Creates a new background task."""
    print("Task creation initiated.")
    try:
        # Generate a unique task ID and validate it
        task_id = str(uuid.uuid4())
        validate_task(task_id, "PENDING")

        # Send the task to Celery
        celery_app.send_task("app.services.task_service.example_task", kwargs={"task_id": task_id})

        # Save the task in the database with PENDING status
        save_task(task_id, "PENDING")
        return {"task_id": task_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while creating task: {e}")


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Fetch the status and result of a background task."""
    try:
        # Validate task_id
        if not task_id or not isinstance(task_id, str):
            raise ValueError("Invalid task_id. Must be a non-empty string.")

        # Check if the task is cached in Redis
        cached_status = await redis_client.hgetall(task_id)
        if cached_status:
            return {
                "task_id": task_id,
                "status": cached_status["status"]
            }

        # If not cached, retrieve the task from the database
        task = get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task Not Found")

        status = task["status"]

        # Cache the task in Redis
        await redis_client.hset(task_id, mapping={"status": status})
        await redis_client.expire(task_id, 3600)  # Set TTL to 1 hour

        return {"task_id": task_id, "status": status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching task: {e}")
