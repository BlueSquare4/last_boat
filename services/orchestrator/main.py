from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.orchestrator.agent import orchestrator
import uvicorn

app = FastAPI(title="Orchestrator")

class QueryRequest(BaseModel):
    query: str
    propertyId: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orchestrator"}

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        user_input = request.query
        if request.propertyId:
            full_prompt = f"{user_input}\n[GA4 Property ID: {request.propertyId}]"
        else:
            full_prompt = user_input
        
        response = orchestrator.run(full_prompt)
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
