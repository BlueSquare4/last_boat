from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
import os
import sys

# Ensure we can import shared
sys.path.append(os.getcwd())
from shared.llm import get_model_name

# A2A Agent Configuration
ANALYTICS_HOST = "http://localhost:8001"
SEO_HOST = "http://localhost:8002"

# Define Remote Clients
analytics_client = RemoteA2aAgent(
    name="analytics",
    description="Dedicated expert for Google Analytics 4 (GA4) data. Use this for questions about traffic, users, sessions, page views, and dimensions/metrics.",
    agent_card=f"{ANALYTICS_HOST}/a2a/analytics{AGENT_CARD_WELL_KNOWN_PATH}"
)

seo_client = RemoteA2aAgent(
    name="seo",
    description="Dedicated expert for Technical SEO audits and Screaming Frog data. Use this for questions about site health, missing titles, status codes, and crawl data.",
    agent_card=f"{SEO_HOST}/a2a/seo{AGENT_CARD_WELL_KNOWN_PATH}"
)

# Define Orchestrator
# This agent takes the user query and routes it to the appropriate sub-agent(s).
orchestrator = LlmAgent.builder() \
    .name("orchestrator") \
    .model("gemini-1.5-pro") \
    .subAgents([analytics_client, seo_client]) \
    .instruction("You are a smart Orchestrator. You receive a user query and possibly a context (Property ID). "
                 "Your goal is to answer the user's question by delegating work to your specialized experts: 'analytics' and 'seo'. "
                 "If the question implies both (e.g. 'top pages by views and their title tags'), ask both agents and synthesize the answer. "
                 "If the question is simple, route it directly. "
                 "Always provide a final answer in natural language unless JSON is explicitly requested.") \
    .build()
