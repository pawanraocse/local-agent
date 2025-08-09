#!/bin/bash
# Script to build Docker image, start services, and run tests inside the container
set -e
export ENV_FILE=.env.test
export PYTEST_CURRENT_TEST=1

IMAGE_NAME="local-agent-app"
OLLAMA_HOST="http://localhost:11434"

# Ensure test-reports directory exists on host BEFORE starting docker-compose
mkdir -p ./test-reports

# If docker-compose is already running, bring it down first for a clean start
if docker-compose ps | grep -q 'support-bot'; then
  echo "Stopping existing docker-compose services..."
  docker-compose down
fi

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Start all services with docker-compose
echo "Starting all services with docker-compose..."
docker-compose up -d

# Health check for Ollama service
function check_ollama_health() {
  echo "Checking Ollama service health at $OLLAMA_HOST..."
  for i in {1..10}; do
    if curl -s "$OLLAMA_HOST/api/tags" | grep -q '"models"'; then
      echo "Ollama service is healthy."
      return 0
    fi
    echo "Waiting for Ollama service... ($i/10)"
    sleep 2
  done
  echo "Ollama service is not healthy or not running. Aborting tests."
  docker-compose down
  exit 1
}

# Run Ollama health check before tests
check_ollama_health

# Run tests inside the running support-bot container from project root with PYTHONPATH set
echo "Running pytest in Docker container..."
docker exec support-bot pytest tests -v --maxfail=1 --disable-warnings --tb=short --html=/app/test-reports/report.html

# Print contents of test-reports to verify report generation
echo "Contents of ./test-reports after test run:"
ls -l ./test-reports

# Optionally bring down services after tests (always in final block)
echo "Bringing down all services..."
docker-compose down

# Exit with pytest status
exit $?
