#!/bin/bash

# Railway deployment script
set -e

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data static/reports

# Start Ollama in background (if available)
# Note: On Railway, you might need Ollama as a separate service

# Run the application
python app.py