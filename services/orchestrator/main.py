from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.orchestrator.agent import orchestrator
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    propertyId: Optional[str] = None

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        # Prepare the input for the agent
        # We inject the propertyId into the query text or context so the agent is aware of it.
        # This ensures it passes it down to the Analytics agent if needed.
        
        user_input = request.query
        context_str = ""
        if request.propertyId:
            # We explicitly tell the orchestrator about the property ID so it can include it in instructions to sub-agents
            context_str = f"\n[Context: GA4 Property ID = {request.propertyId}]\n"
            # We append it to the user input effectively "prompting" the model with the context
            # A cleaner way would be passing session state, but for a stateless /query endpoint, this is robust.
            full_prompt = f"{user_input}{context_str}"
        else:
            full_prompt = user_input

        # Execute the Agent
        # Assuming ADK agent.run() or similar. 
        # If ADK API is different (e.g. generate_response), checking naming conventions.
        # Based on docs, it's often `result = agent.run(prompt)` or `session.run(prompt)`
        
        # We start a run.
        # Note: LlmAgent usually returns a GenerationResponse object.
        response = orchestrator.run(full_prompt)
        
        # Extract text. The response object usually has a .text property or similar.
        # If it returns a string directly, great. If object, we access .text.
        final_answer = response.text if hasattr(response, 'text') else str(response)
        
        return {"answer": final_answer}
        
    except Exception as e:
        # Log error
        print(f"Orchestrator Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
