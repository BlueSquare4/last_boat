import json
from google.analytics.data_v1beta import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)

from app.llm.client import llm_chat
from app.ga4.client import get_ga4_client
from app.ga4.validator import validate_plan


def infer_ga4_plan(query: str) -> dict:
    prompt = f"""
You are a Google Analytics 4 expert.

Convert the following question into a GA4 reporting plan.

Rules:
- Use valid GA4 metric and dimension names
- Infer date ranges correctly
- Do NOT explain anything
- Output ONLY valid JSON

JSON schema:
{{
  "metrics": [],
  "dimensions": [],
  "start_date": "YYYY-MM-DD or NdDaysAgo",
  "end_date": "today"
}}

User query:
{query}
"""
    response = llm_chat([{"role": "user", "content": prompt}])
    return json.loads(response)


def run_analytics_query(property_id: str, query: str):
    plan = infer_ga4_plan(query)
    metrics, dimensions = validate_plan(plan)

    client = get_ga4_client()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[
            DateRange(
                start_date=plan["start_date"],
                end_date=plan["end_date"]
            )
        ],
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in dimensions]
    )

    return client.run_report(request)


def explain_response(response, query: str) -> str:
    if not response.rows:
        return "No data is available for this GA4 property in the selected date range."

    prompt = f"""
User question:
{query}

GA4 raw response:
{response}

Explain the insights clearly and concisely for a business user.
"""
    return llm_chat([{"role": "user", "content": prompt})
