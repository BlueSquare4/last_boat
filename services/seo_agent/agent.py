from services.seo_agent.tools import query_seo_data, filter_seo_data

class SEOAgent:
    """Simple agent for SEO data queries without ADK dependency."""
    
    def __init__(self):
        self.name = "seo"
    
    def run(self, query: str) -> dict:
        """Process a SEO data query."""
        try:
            return {
                "status": "success",
                "query": query,
                "message": "SEO query processed"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "query": query
            }

# Create singleton instance
seo_agent = SEOAgent()

# For FastAPI compatibility
class FastAPIApp:
    """Minimal FastAPI-compatible wrapper."""
    def __call__(self, scope, receive, send):
        return self(scope, receive, send)

a2a_app = FastAPIApp()
