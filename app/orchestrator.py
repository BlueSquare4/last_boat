from app.agents.analytics_agent import run_analytics_query, explain_response

def handle_query(payload: dict):
    query = payload.get("query")
    property_id = payload.get("propertyId")

    if property_id:
        response = run_analytics_query(property_id, query)
        explanation = explain_response(response, query)

        return {
            "type": "analytics",
            "explanation": explanation,
            "rowCount": len(response.rows),
            "data": [
                {
                    "dimensions": [v.value for v in row.dimension_values],
                    "metrics": [v.value for v in row.metric_values]
                }
                for row in response.rows
            ]
        }

    return {"error": "No propertyId provided for analytics query"}
