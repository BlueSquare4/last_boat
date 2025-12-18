from fastapi import FastAPI, HTTPException
from app.orchestrator import handle_query

app = FastAPI()

@app.post("/query")
def query_handler(payload: dict):
    try:
        return handle_query(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
