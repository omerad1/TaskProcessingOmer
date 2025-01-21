#!/bin/bash

# Start Redis
echo "Starting Redis server..."
redis-server &

# Start Celery worker
echo "Starting Celery worker..."
celery -A celery_app.celery_config worker --loglevel=info &

# Start FastAPI application
echo "Starting FastAPI server..."
uvicorn app.main:app --reload
