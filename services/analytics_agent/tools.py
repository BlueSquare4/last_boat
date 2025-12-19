import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    FilterExpression,
)
from google.oauth2 import service_account

# Allowlist for Tier 1 Safety Validation
ALLOWED_METRICS = {
    "activeUsers", "sessions", "screenPageViews", "eventCount", "totalUsers", "newUsers"
}
ALLOWED_DIMENSIONS = {
    "date", "city", "country", "pagePath", "eventName", "deviceCategory", "platform", "dayOfWeek"
}

def get_ga4_client():
    """
    Creates a GA4 client using credentials.json from the project root.
    Reloads on every call to ensure evaluator updates are picked up.
    """
    creds_path = os.path.join(os.getcwd(), "credentials.json")
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"credentials.json not found at {creds_path}")
    
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    return BetaAnalyticsDataClient(credentials=credentials)

def run_ga4_report(property_id: str, dimensions: list[str], metrics: list[str], start_date: str, end_date: str):
    """
    Executes a GA4 report.
    
    Args:
        property_id: The GA4 Property ID.
        dimensions: List of dimension names (e.g., ['date', 'pagePath']).
        metrics: List of metric names (e.g., ['activeUsers']).
        start_date: Start date (YYYY-MM-DD or '30daysAgo').
        end_date: End date (YYYY-MM-DD or 'today').
    """
    # Validation
    for m in metrics:
        if m not in ALLOWED_METRICS:
            raise ValueError(f"Metric '{m}' is not allowed. Allowed: {ALLOWED_METRICS}")
    for d in dimensions:
        if d not in ALLOWED_DIMENSIONS:
            raise ValueError(f"Dimension '{d}' is not allowed. Allowed: {ALLOWED_DIMENSIONS}")

    client = get_ga4_client()
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    
    response = client.run_report(request)
    
    # Parse Response into simple JSON-serializable format
    result = []
    for row in response.rows:
        item = {}
        for i, dimension_value in enumerate(row.dimension_values):
            item[dimensions[i]] = dimension_value.value
        for i, metric_value in enumerate(row.metric_values):
            # Try to convert to int/float if possible
            try:
                val = float(metric_value.value)
                if val.is_integer():
                    val = int(val)
            except ValueError:
                val = metric_value.value
            item[metrics[i]] = val
        result.append(item)
        
    return result
