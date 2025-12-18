# GA4 Analytics Agent – Spike AI Hackathon

## Overview
This service implements a production-ready GA4 Analytics Agent capable of answering natural-language questions using live Google Analytics 4 data.

## Architecture
- FastAPI single POST endpoint
- Orchestrator-based routing
- GA4 Analytics Agent (Tier 1)
- Gemini LLM via LiteLLM proxy
- Google Analytics Data API

## Endpoint
POST `/query`

```json
{
  "propertyId": "123456789",
  "query": "Give me daily page views for the last 14 days"
}