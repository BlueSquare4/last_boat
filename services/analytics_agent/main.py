import uvicorn
from services.analytics_agent.agent import a2a_app

# This file is just an entry point for the uvicorn worker in deploy.sh
if __name__ == "__main__":
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
