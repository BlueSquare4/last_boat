import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)
from google.oauth2 import service_account

# Allowlist for Safety Validation
ALLOWED_METRICS = {
    "activeUsers", "sessions", "screenPageViews", "eventCount", "totalUsers", "newUsers"
}
ALLOWED_DIMENSIONS = {
    "date", "city", "country", "pagePath", "eventName", "deviceCategory", "platform", "dayOfWeek"
}

def get_ga4_client():
    """Creates a GA4 client using credentials.json."""
    creds_path = os.path.join(os.getcwd(), "credentials.json")
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"credentials.json not found at {creds_path}. Please add your GA4 service account credentials.")
    
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    return BetaAnalyticsDataClient(credentials=credentials)

def run_ga4_report(property_id: str, dimensions: list, metrics: list, start_date: str, end_date: str) -> list:
    """Execute a GA4 report with validated metrics and dimensions."""
    
    # Validate inputs
    for m in metrics:
        if m not in ALLOWED_METRICS:
            raise ValueError(f"Metric '{m}' not allowed. Allowed: {ALLOWED_METRICS}")
    for d in dimensions:
        if d not in ALLOWED_DIMENSIONS:
            raise ValueError(f"Dimension '{d}' not allowed. Allowed: {ALLOWED_DIMENSIONS}")

    client = get_ga4_client()
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    
    response = client.run_report(request)
    
    # Parse response into JSON-serializable format
    result = []
    for row in response.rows:
        item = {}
        for i, dimension_value in enumerate(row.dimension_values):
            item[dimensions[i]] = dimension_value.value
        for i, metric_value in enumerate(row.metric_values):
            try:
                val = float(metric_value.value)
                item[metrics[i]] = int(val) if val.is_integer() else val
            except (ValueError, AttributeError):
                item[metrics[i]] = metric_value.value
        result.append(item)
        
    return result
