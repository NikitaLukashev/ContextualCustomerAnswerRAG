.PHONY: help test test-local test-docker test-clean build-test build-app up down logs

# Default target
help:
	@echo "Available commands:"
	@echo "  test          - Run tests in Docker containers (default)"
	@echo "  test-local    - Run tests locally (requires running services)"
	@echo "  test-docker   - Run tests in Docker containers"
	@echo "  test-clean    - Clean up test containers and volumes"
	@echo "  build-test    - Build test Docker image"
	@echo "  build-app     - Build main application Docker image"
	@echo "  up            - Start main services"
	@echo "  down          - Stop all services"
	@echo "  logs          - Show logs from main services"



# Build test Docker image
build-test:
	@echo "🔨 Building test Docker image..."
	docker build -f Dockerfile.test -t rag-system-test .

# Build main application Docker image
build-app:
	@echo "🔨 Building main application Docker image..."
	docker build -t rag-system-app .

# Start main services
up:
	@echo "🚀 Starting main services..."
	docker-compose up -d

# Run tests in Docker containers
test-docker:
	@echo "🐳 Running tests in Docker containers..."
	docker-compose -f docker-compose.test.yml up


# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker-compose down

# Show logs from main services
logs:
	@echo "📋 Showing logs from main services..."
	docker-compose logs -f

# Quick test (build and run tests)
quick-test: build-test test-docker

# Full test cycle (build everything and run tests)
full-test: build-app build-test test-docker
