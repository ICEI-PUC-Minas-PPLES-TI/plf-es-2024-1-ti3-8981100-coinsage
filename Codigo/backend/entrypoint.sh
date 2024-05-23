#!/bin/sh

# Apply database migrations
echo "Running database migrations..."
alembic revision --autogenerate -m "Initial" && alembic upgrade head

# Start the application
echo "Starting the application..."
uvicorn src.main:backend_app --workers 4 --host 0.0.0.0 --port 8000
