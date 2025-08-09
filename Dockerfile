FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy application code
COPY app/ .
COPY tests/ ./tests

# Create documents directory
RUN mkdir -p /app/documents

# Set PYTHONPATH to /app
ENV PYTHONPATH=/app

# Default command runs the app
CMD ["python", "main.py"]

# Test command (can be run with: docker build --target test ... or docker run ... pytest)
# Uncomment below to run tests automatically on build
# RUN pytest --maxfail=1 --disable-warnings --tb=short
