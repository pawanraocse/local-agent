"""
Configuration module for model, database, and service endpoints.
Handles environment-based overrides for test speed and traceability.
"""

import os
import logging

# Structured logging setup
logger = logging.getLogger("config")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
print("CONFIG LOADED: logging configured for 'config' logger")

# Detect test environment and override model if needed
# Enhanced logging for model selection
if os.getenv("PYTEST_CURRENT_TEST") or not os.getenv("OLLAMA_MODEL"):
    logger.info("[CONFIG] Detected test environment (PYTEST_CURRENT_TEST set) or OLLAMA_MODEL not set. Using lightweight model: 'qwen2.5-coder:0.5b' for OLLAMA_MODEL.")
    MODEL_NAME = "qwen2.5-coder:0.5b"
else:
    MODEL_NAME = os.getenv("OLLAMA_MODEL")
    if not MODEL_NAME:
        logger.warning("[CONFIG] OLLAMA_MODEL not set in environment; defaulting to 'codellama:7b'.")
        MODEL_NAME = "codellama:7b"
    else:
        logger.info(f"[CONFIG] Using OLLAMA_MODEL from environment: {MODEL_NAME}")

# Ollama service configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
if not OLLAMA_HOST:
    logger.warning("OLLAMA_HOST not set in environment; defaulting to 'http://ollama:11434'.")
    OLLAMA_HOST = "http://ollama:11434"  # Use Docker Compose service name for inter-container networking
else:
    logger.info(f"Using OLLAMA_HOST: {OLLAMA_HOST}")

# ChromaDB collection configuration
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION")
if not CHROMA_COLLECTION:
    logger.warning("CHROMA_COLLECTION not set in environment; defaulting to 'agent_history'.")
    CHROMA_COLLECTION = "agent_history"
else:
    logger.info(f"Using CHROMA_COLLECTION: {CHROMA_COLLECTION}")
