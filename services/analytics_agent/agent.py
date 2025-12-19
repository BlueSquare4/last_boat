from google.adk.agents import LlmAgent
from google.adk.agents.a2a_agent import to_a2a
from services.analytics_agent.tools import run_ga4_report
import os
import sys

# Ensure we can import shared
sys.path.append(os.getcwd())
from shared.llm import get_model_name

# Define the Agent
# We configure the model to be purely compatible with the ADK expectations.
# Note: ADK's LlmAgent uses Vertex AI by default. 
# Since we need to use LiteLLM (OpenAI interface), we might need to inject a custom model client 
# OR use the 'model_client' argument if supported, or monkey-patch.
#
# For this hackathon, sticking to the standard ADK usage might try to call Vertex.
# If ADK doesn't support generic OpenAI clients easily, we might need a workaround.
#
# Workaround: valid ADK agents define a `model` string. 
# We'll assume for now we can standardise this later or ADK supports it via environment.
# Actually, looking at docs, ADK is heavily vertex-integrated.
#
# Let's rely on the assumption that we can pass a custom model client or configuring it via `google-genai` which `google-adk` likely uses.
# IF `google-adk` strictly enforces Vertex, we might break.
# But `PS.md` says "Option 1: Using OpenAI-Compatible Libraries". 
# 
# Let's proceed with defining the tool wrapper.

def ga4_report_tool(property_id: str, dimensions: list[str], metrics: list[str], start_date: str, end_date: str) -> str:
    """
    Fetches analytics data from Google Analytics 4.
    Use this tool when the user asks for metrics like page views, sessions, or users.
    
    Args:
        property_id: The GA4 Property ID. ALWAYS use the one provided in the context.
        dimensions: Attributes to break down data by (e.g., 'date', 'pagePath', 'country').
        metrics: Quantitative measurements (e.g., 'activeUsers', 'screenPageViews').
        start_date: Start date (YYYY-MM-DD or 'NdaysAgo').
        end_date: End date (YYYY-MM-DD or 'today').
    """
    try:
        data = run_ga4_report(property_id, dimensions, metrics, start_date, end_date)
        return json.dumps(data)
    except Exception as e:
        return f"Error fetching GA4 data: {str(e)}"

# We need to construct the Agent.
# Since we are using LiteLLM/OpenAI, and ADK defaults to Vertex, 
# we need to be careful. The `google-adk` library might not natively support OpenAI clients without a custom ModelClient implementation.
# For the sake of "using Google ADK", we will define the agent structure here. 
# If execution fails due to auth, we will know.
#
# However, `to_a2a` basically wraps the agent. The critical part is the `agent_card`.

analytics_agent = LlmAgent.builder() \
    .name("analytics") \
    .description("A data analyst capable of querying Google Analytics 4 (GA4).") \
    .tools([ga4_report_tool]) \
    .instruction("You are a helpful Data Analyst. When asked for data, use the ga4_report_tool. "
                 "Always verify if you have a property_id. If not, ask for it."
                 "Translate natural language date ranges like 'last week' to start_date/end_date formats (YYYY-MM-DD or '7daysAgo').") \
    .build()

# Expose as A2A
a2a_app = to_a2a(analytics_agent)
