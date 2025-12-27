.PHONY: start stop rebuild clean test test-backend test-frontend logs dev install

# Docker commands
start:
	docker-compose up -d

stop:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose up --build -d

clean:
	docker-compose down -v
	docker system prune -f

# Test commands
test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest -v

test-frontend:
	cd frontend && npm test

# Development (local without Docker)
dev:
	npm run dev

# Install dependencies
install:
	npm run install:all

# View logs
logs:
	docker-compose logs -f app

# Help
help:
	@echo "Available commands:"
	@echo "  make start         - Start the app (Docker)"
	@echo "  make stop          - Stop the app (Docker)"
	@echo "  make rebuild       - Rebuild and start Docker containers"
	@echo "  make clean         - Stop containers and remove volumes/cache"
	@echo "  make test          - Run all tests"
	@echo "  make test-backend  - Run backend tests (pytest)"
	@echo "  make test-frontend - Run frontend tests (vitest)"
	@echo "  make dev           - Start local development servers"
	@echo "  make install       - Install all dependencies"
	@echo "  make logs          - View Docker logs"
