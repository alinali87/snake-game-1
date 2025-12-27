# Multi-stage build for Snake Game
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Install nginx and system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for faster Python package installation
RUN pip install uv

# Copy backend dependencies and install
COPY backend/requirements.txt ./backend/
RUN cd backend && uv pip install --system -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for nginx logs and runtime
RUN mkdir -p /var/log/nginx /var/lib/nginx/body /var/lib/nginx/fastcgi \
    /var/lib/nginx/proxy /var/lib/nginx/scgi /var/lib/nginx/uwsgi

# Expose port
EXPOSE 8080

# Copy startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app/backend

ENTRYPOINT ["/docker-entrypoint.sh"]
