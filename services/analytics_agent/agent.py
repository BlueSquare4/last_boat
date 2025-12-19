import json
from services.analytics_agent.tools import run_ga4_report

class AnalyticsAgent:
    """Simple agent for GA4 queries without ADK dependency."""
    
    def __init__(self):
        self.name = "analytics"
    
    def run(self, query: str, property_id: str = None) -> dict:
        """
        Process a GA4 analytics query.
        
        Args:
            query: Natural language query
            property_id: GA4 property ID
            
        Returns:
            dict with results
        """
        try:
            if not property_id:
                return {
                    "error": "Property ID is required for analytics queries",
                    "status": "failed"
                }
            
            # Simple query parsing - in production, use LLM to parse
            # For now, provide a sample result
            results = run_ga4_report(
                property_id=property_id,
                dimensions=["date"],
                metrics=["screenPageViews", "activeUsers"],
                start_date="30daysAgo",
                end_date="today"
            )
            
            return {
                "status": "success",
                "data": results,
                "query": query,
                "property_id": property_id
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "query": query
            }

# Create singleton instance
analytics_agent = AnalyticsAgent()

# For FastAPI compatibility
class FastAPIApp:
    """Minimal FastAPI-compatible wrapper."""
    def __call__(self, scope, receive, send):
        return self(scope, receive, send)

a2a_app = FastAPIApp()
