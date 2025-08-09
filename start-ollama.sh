#!/bin/bash

# Constants
LOG_PREFIX="[OLLAMA INIT]"
MAX_RETRIES=30
RETRY_INTERVAL=2

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $LOG_PREFIX [$1] $2"
}

# Validate environment variable
if [ -z "$OLLAMA_MODEL" ]; then
    log "ERROR" "OLLAMA_MODEL environment variable is not set. Exiting."
    exit 2
fi
MODEL_NAME="$OLLAMA_MODEL"

# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
log "INFO" "Waiting for Ollama to start..."
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
    if ollama list > /dev/null 2>&1; then
        log "INFO" "Ollama service is ready."
        break
    fi
    log "INFO" "Waiting for Ollama service... (attempt $((retry_count + 1))/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $MAX_RETRIES ]; then
    log "ERROR" "Failed to connect to Ollama service after $MAX_RETRIES attempts."
    exit 1
fi

# Only install the model from .env if not already installed
if ! ollama list | grep -q "^$MODEL_NAME"; then
    log "INFO" "Model $MODEL_NAME not found. Installing..."
    ollama pull "$MODEL_NAME"
    if [ $? -ne 0 ]; then
        log "ERROR" "Failed to install model $MODEL_NAME."
        exit 3
    fi
else
    log "INFO" "Model $MODEL_NAME is already installed."
fi

# Keep the container running
wait
