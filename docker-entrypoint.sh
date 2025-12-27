#!/bin/bash
set -e

echo "Starting Snake Game Application..."

# Wait for PostgreSQL to be ready
if [ "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL..."
    until pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}"; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is up!"
fi

# Start nginx
echo "Starting nginx..."
nginx

# Start FastAPI backend
echo "Starting FastAPI backend..."
exec uvicorn main:app --host 127.0.0.1 --port 3000 --workers 2
