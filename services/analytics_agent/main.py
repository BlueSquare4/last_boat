from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Analytics Agent")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "analytics_agent"}

@app.post("/query")
async def query(payload: dict):
    """Analytics query endpoint."""
    try:
        query_text = payload.get("query", "")
        property_id = payload.get("propertyId", "")
        
        if not property_id:
            return {"error": "propertyId is required", "status": "failed"}
        
        return {
            "status": "success",
            "query": query_text,
            "property_id": property_id,
            "message": "Analytics query processed"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
