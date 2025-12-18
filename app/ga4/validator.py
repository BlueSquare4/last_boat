from app.ga4.schema import ALLOWED_METRICS, ALLOWED_DIMENSIONS

def validate_plan(plan: dict):
    metrics = [m for m in plan.get("metrics", []) if m in ALLOWED_METRICS]
    dimensions = [d for d in plan.get("dimensions", []) if d in ALLOWED_DIMENSIONS]

    if not metrics:
        raise ValueError("No valid GA4 metrics inferred")

    return metrics, dimensions
