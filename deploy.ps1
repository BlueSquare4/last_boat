# PowerShell deployment script for Windows

Write-Host "Deploying Spike AI Analytics Services..." -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start Services in new windows
Write-Host "Starting services..." -ForegroundColor Green

# 1. Analytics Agent (Port 8001)
Write-Host "Starting Analytics Agent on Port 8001..." -ForegroundColor Cyan
Start-Process -FilePath python -ArgumentList "-m uvicorn services.analytics_agent.main:app --host 0.0.0.0 --port 8001"

# 2. SEO Agent (Port 8002)
Write-Host "Starting SEO Agent on Port 8002..." -ForegroundColor Cyan
Start-Process -FilePath python -ArgumentList "-m uvicorn services.seo_agent.main:app --host 0.0.0.0 --port 8002"

# Wait for services to start
Start-Sleep -Seconds 3

# 3. Orchestrator (Port 8080)
Write-Host "Starting Orchestrator on Port 8080..." -ForegroundColor Green
Write-Host "Services started! Orchestrator running on http://localhost:8080" -ForegroundColor Green
python -m uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8080
