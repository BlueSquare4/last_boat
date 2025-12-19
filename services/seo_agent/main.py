from fastapi import FastAPI
import uvicorn

app = FastAPI(title="SEO Agent")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "seo_agent"}

@app.post("/query")
async def query(payload: dict):
    """SEO query endpoint."""
    try:
        query_text = payload.get("query", "")
        return {
            "status": "success",
            "query": query_text,
            "message": "SEO query processed"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
