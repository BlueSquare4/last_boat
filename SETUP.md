# Spike AI Analytics Platform

A multi-agent system for Google Analytics 4 (GA4) and SEO data analysis.

## Architecture

Three FastAPI services running on different ports:
- **Analytics Agent** (Port 8001): Handles GA4 queries
- **SEO Agent** (Port 8002): Handles SEO audit data queries
- **Orchestrator** (Port 8080): Routes requests to appropriate agents

## Setup

### 1. Prerequisites
- Python 3.10+
- Google Analytics 4 credentials (optional, for GA4 features)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file from the template:
```bash
copy .env.template .env
```

Then edit `.env` with your credentials:
```
LLM_API_KEY=your-openai-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

### 4. (Optional) GA4 Setup
To use GA4 features, place your `credentials.json` file in the project root:
```
credentials.json  # Google service account credentials
```

## Running the Services

### Windows PowerShell
```powershell
.\deploy.ps1
```

This will:
1. Start Analytics Agent on port 8001
2. Start SEO Agent on port 8002  
3. Start Orchestrator on port 8080

### Manual Start (Any OS)
Terminal 1 - Analytics Agent:
```bash
python -m uvicorn services.analytics_agent.main:app --host 0.0.0.0 --port 8001
```

Terminal 2 - SEO Agent:
```bash
python -m uvicorn services.seo_agent.main:app --host 0.0.0.0 --port 8002
```

Terminal 3 - Orchestrator:
```bash
python -m uvicorn services.orchestrator.main:app --host 0.0.0.0 --port 8080
```

## API Usage

### Health Check
```bash
curl http://localhost:8080/health
```

### Query Orchestrator
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my top pages?", "propertyId": "123456789"}'
```

## File Structure

```
services/
├── analytics_agent/          # GA4 analytics queries
│   ├── main.py              # FastAPI app entry point
│   ├── agent.py             # Analytics logic
│   └── tools.py             # GA4 API utilities
├── seo_agent/               # SEO audit queries
│   ├── main.py              # FastAPI app entry point
│   ├── agent.py             # SEO logic
│   └── tools.py             # SEO data utilities
└── orchestrator/            # Request router
    ├── main.py              # FastAPI app entry point
    └── agent.py             # Routing logic

shared/
└── llm.py                   # LLM client configuration

requirements.txt             # Python dependencies
.env.template               # Environment variable template
deploy.ps1                  # Windows deployment script
```

## Removed/Cleaned Up

- **Removed**: `app/` folder (was duplicate of `services/`)
- **Removed**: Non-existent dependencies (`google-adk`, `a2a-sdk`)
- **Removed**: Hardcoded credentials
- **Simplified**: All agent implementations to work without external ADK libraries
- **Cleaned**: Unused imports and dead code

## Features

✓ Multi-agent architecture with clean separation  
✓ Simple HTTP routing between services  
✓ GA4 data query support (with credentials)  
✓ SEO audit data analysis  
✓ Environment-based configuration  
✓ Health check endpoints  
✓ Error handling and logging  

## Troubleshooting

**Port already in use?**
```bash
# Find and kill process on port 8080
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**Missing .env file?**
```bash
copy .env.template .env
# Edit .env with your API keys
```

## License

Hackathon Project - Spike AI 2025
