from pydantic import BaseModel

''' Defines a data model for tasks to ensure consistent and structed data for 
tasks responses'''
''' pydantic is designed to provide data validation
and settings management using type annotation'''
''' using basemodel to provide foundation for creating models that define and validate data structures'''


class TaskStatus(BaseModel):
    task_id: str  # unique identifier
    status: str  # current status of the task
    result: dict | None = None  # result of the task
