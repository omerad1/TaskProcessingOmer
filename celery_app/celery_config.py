from celery import Celery

celery_app = Celery(
    "app",
    broker="redis://localhost:6379/0",  # Redis as broker
    backend="redis://localhost:6379/0"  # Redis as backend
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True
)

# Import the task to ensure it is registered
from app.services.task_service import example_task