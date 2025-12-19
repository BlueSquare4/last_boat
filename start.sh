#!/bin/bash
# Quick start script for Linux/Mac users

echo "====================================="
echo "Spike AI Analytics - Quick Start"
echo "====================================="

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.template .env
    echo "Please edit .env with your API keys"
fi

echo ""
echo "Starting services..."
echo ""

# Start services in background
python -m uvicorn services.analytics_agent.main:app --host 0.0.0.0 --port 8001 &
echo "✓ Analytics Agent on port 8001"

python -m uvicorn services.seo_agent.main:app --host 0.0.0.0 --port 8002 &
echo "✓ SEO Agent on port 8002"

sleep 2

echo ""
echo "Starting Orchestrator..."
python -m uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8080

echo ""
echo "All services running!"
echo "Orchestrator API: http://localhost:8080"
echo ""
