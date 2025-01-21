# Task Processing with FastAPI and Celery

A FastAPI-based API to manage and track background tasks using Celery and Redis.
The application allows creating and querying tasks, 
storing their statuses in an SQLite database, and caching them in Redis for quick access.

## Features

- **Task Management**: Create and track the status of tasks.
- **Asynchronous Background Tasks**: Handle long-running tasks using Celery.
- **Redis Integration**: Cache task statuses for faster access.
- **SQLite Database**: Persist task information.
- **Simple Deployment**: Use the `run.sh` script to start the entire system.

## Prerequisites

- Python 3.10+
- Redis (installed on your system)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/omerad1/TaskProcessingOmer.git
    cd TaskProcessingOmer
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Make the `run.sh` script executable:
    ```bash
    chmod +x run.sh
    ```

2. Run the script to start Redis, Celery, and the FastAPI server:
    ```bash
    ./run.sh
    ```

3. Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000) and run requests via [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Endpoints

- **Create Task**: `POST /tasks/`
    - Request: No body required.
    - Example Response:
      ```json
      {
        "task_id": "123e4567-e89b-12d3-a456-426614174000"
      }
      ```

- **Get Task Status**: `GET /tasks/{task_id}`
    - Path Parameter:
      - `task_id`: The unique identifier of the task.
    - Example Response:
      ```json
      {
        "task_id": "123e4567-e89b-12d3-a456-426614174000",
        "status": "PENDING"
      }
      ```

## Running Tests

1. Run tests:
    ```bash
    pytest tests/
    ```
