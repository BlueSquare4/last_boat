from google.adk.agents import LlmAgent
from google.adk.agents.a2a_agent import to_a2a
from services.seo_agent.tools import query_seo_data, filter_seo_data
import os
import sys

# Ensure we can import shared
sys.path.append(os.getcwd())

# Define the Agent
seo_agent = LlmAgent.builder() \
    .name("seo") \
    .description("An SEO technical expert capable of analyzing raw crawl data.") \
    .tools([query_seo_data, filter_seo_data]) \
    .instruction("You are a Technical SEO expert. You have access to a crawl provided in a spreadsheet. "
                 "Use 'query_seo_data' to inspect the schema/columns first. "
                 "Use 'filter_seo_data' to find specific pages (e.g., missing titles, non-https). "
                 "Combine multiple filter steps if needed to answer complex questions.") \
    .build()

# Expose as A2A
a2a_app = to_a2a(seo_agent)
