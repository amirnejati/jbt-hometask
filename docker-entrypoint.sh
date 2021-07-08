# Apply database migrations
alembic upgrade head

echo "Starting server ..."
uvicorn main:app --host 0.0.0.0 --port 8080
