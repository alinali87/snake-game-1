#!/bin/bash
set -e

echo "Starting Snake Game Application..."

# Parse DATABASE_URL for pg_isready if it's a full connection string
if [ "$DATABASE_URL" ]; then
    echo "Database URL detected, checking connection..."

    # Extract host from DATABASE_URL (handles both postgres:// and postgresql://)
    DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
    DB_PORT=$(echo "$DATABASE_URL" | sed -E 's|.*:([0-9]+)/.*|\1|' | grep -E '^[0-9]+$' || echo "5432")

    # Only run pg_isready for local/docker PostgreSQL (not external managed databases like Render)
    if [ "$POSTGRES_HOST" ] && [ "$POSTGRES_HOST" != "localhost" ]; then
        echo "Using external managed PostgreSQL at $DB_HOST - skipping pg_isready"
    else
        echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
        for i in {1..30}; do
            if pg_isready -h "$DB_HOST" -p "$DB_PORT" 2>/dev/null; then
                echo "PostgreSQL is up!"
                break
            fi
            if [ $i -eq 30 ]; then
                echo "Warning: Could not verify PostgreSQL connection, proceeding anyway..."
            fi
            sleep 2
        done
    fi
fi

# Use PORT environment variable if set (for cloud platforms like Render)
NGINX_PORT="${PORT:-8080}"

# Update nginx to listen on the correct port
if [ "$NGINX_PORT" != "8080" ]; then
    echo "Configuring nginx to listen on port $NGINX_PORT..."
    sed -i "s/listen 8080/listen $NGINX_PORT/g" /etc/nginx/nginx.conf
fi

# Start nginx
echo "Starting nginx on port $NGINX_PORT..."
nginx

# Start FastAPI backend
echo "Starting FastAPI backend..."
exec uvicorn main:app --host 127.0.0.1 --port 3000 --workers 2
