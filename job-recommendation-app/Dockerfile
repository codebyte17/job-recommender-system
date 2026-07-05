FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (important for many packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements FIRST (better Docker caching)
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY backend/ backend/
COPY recommendation_engine/ recommendation_engine/

# Make Python see both modules
ENV PYTHONPATH=/app

# Prevent buffering logs (important for Docker logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend