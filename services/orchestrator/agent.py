import httpx
import json
from shared.llm import get_openai_client, get_model_name

class Orchestrator:
    """Routes queries to appropriate sub-agents."""
    
    def __init__(self):
        self.name = "orchestrator"
        self.analytics_url = "http://localhost:8001/query"
        self.seo_url = "http://localhost:8002/query"
        self.llm_client = get_openai_client()
        self.model = get_model_name()
    
    def run(self, prompt: str) -> dict:
        """Process a query and route to appropriate agent."""
        try:
            # Route query to appropriate service
            # For now, default to analytics if property ID mentioned, else SEO
            
            if "property" in prompt.lower() or "ga4" in prompt.lower() or "analytics" in prompt.lower():
                response = self._query_analytics(prompt)
            elif "seo" in prompt.lower() or "crawl" in prompt.lower() or "audit" in prompt.lower():
                response = self._query_seo(prompt)
            else:
                # Default routing
                response = self._query_analytics(prompt)
            
            return response
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _query_analytics(self, query: str) -> dict:
        """Send query to analytics agent."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.analytics_url,
                    json={"query": query},
                    timeout=10.0
                )
                return response.json()
        except Exception as e:
            return {"error": f"Analytics service error: {str(e)}", "status": "failed"}
    
    def _query_seo(self, query: str) -> dict:
        """Send query to SEO agent."""
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.seo_url,
                    json={"query": query},
                    timeout=10.0
                )
                return response.json()
        except Exception as e:
            return {"error": f"SEO service error: {str(e)}", "status": "failed"}

# Create singleton
orchestrator = Orchestrator()
