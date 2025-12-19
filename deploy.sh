#!/bin/bash

# Exit on error
set -e

echo "Deploying Spike AI Builder Solution..."

# install uv
pip install uv

# Install dependencies using uv for speed
echo "Installing dependencies..."
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Start Services
# We use background processes (&) to run multiple services
# 1. Analytics Agent (Port 8001)
echo "Starting Analytics Agent on Port 8001..."
nohup uvicorn services.analytics_agent.main:a2a_app --host 0.0.0.0 --port 8001 > analytics.log 2>&1 &
ANALYTICS_PID=$!

# 2. SEO Agent (Port 8002)
echo "Starting SEO Agent on Port 8002..."
nohup uvicorn services.seo_agent.main:a2a_app --host 0.0.0.0 --port 8002 > seo.log 2>&1 &
SEO_PID=$!

# Wait briefly for agents to spin up
sleep 5

# 3. Architect/Orchestrator (Port 8080)
echo "Starting Orchestrator on Port 8080..."
# This is the main process that keeps the container alive
exec uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8080
