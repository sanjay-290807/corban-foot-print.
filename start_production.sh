#!/bin/bash

# Production deployment script for CarbonIQ

echo "🚀 Starting CarbonIQ Production Deployment..."

# Set environment variables
export FLASK_ENV=production
export PORT=${PORT:-5000}

# Create necessary directories
mkdir -p data static/reports

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
echo "🌐 Starting server on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 wsgi:app