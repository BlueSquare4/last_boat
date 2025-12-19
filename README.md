# Spike AI Architecture: A Google ADK & A2A Powered Microservice System

## 1. Executive Summary

This project implements a production-ready **Mixture of Experts (MoE)** AI backend, designed to answer complex natural language queries about Web Analytics (GA4) and Technical SEO. 

By leveraging **Google's Agent Development Kit (ADK)** and the **Agent-to-Agent (A2A) Protocol**, we have moved beyond a fragile monolithic agent structure to a robust **Microservices Architecture**. This design ensures modularity, scalability, and precise fault isolation, allowing specialized "Expert Agents" to operate independently while being orchestrated by a central intelligent router.

## 2. Architecture: Agents as Microservices

![Architecture Diagram](archi.png)

The system is composed of three distinct microservices, communicating over HTTP using the standardized A2A protocol.

### 2.1 The Orchestrator (Port 8080)
*   **Role**: The "Brain" and public face of the system.
*   **Responsibility**: Receiving user queries via a single `POST /query` endpoint.
*   **Logic**: It does not process data itself. Instead, it uses a Large Language Model (Gemini 1.5 Pro) to classify intent and **route** instructions to the appropriate expert(s).
*   **Composition**: It consumes the downstream agents using `RemoteA2aAgent`, effectively treating remote microservices as local function calls.

### 2.2 The Analytics Expert (Port 8001)
*   **Role**: A specialized agent for Google Analytics 4.
*   **Tools**: Equipped with the GA4 Data API (`BetaAnalyticsDataClient`).
*   **Security**: Runs in its own process. If the GA4 client hangs or crashes, it does not bring down the entire system.
*   **Protocol**: Exposes its capabilities via `.well-known/agent.json` (A2A Standard), allowing the orchestrator to dynamically understand its skills.

### 2.3 The SEO Expert (Port 8002)
*   **Role**: A specialized agent for Technical SEO.
*   **Tools**: Equipped with Pandas/Python logic to ingest and filter Screaming Frog crawl data.
*   **Protocol**: Also exposes an A2A interface.

## 3. Technology Stack

We purposefully chose a highly modular, open-source stack to ensure vendor neutrality and extensibility.

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Framework** | **Google ADK (Python)** | Provides the foundational primitives for building `LlmAgent` and `Tool` definitions in a standard way. |
| **Protocol** | **A2A SDK** | Enables standard discovery and communication between agents. This is key to our microservice approach. |
| **API Layer** | **FastAPI + Uvicorn** | High-performance, async Python web framework. Standard for modern AI microservices. |
| **LLM Interface** | **LiteLLM** | provides a unified interface to call OpenAI-compatible endpoints (used here to proxy to Gemini). |
| **Data Processing** | **Pandas & Google Analytics Data API** | Industry-standard libraries for data manipulation. |

## 4. Why Microservices? (Superiority over Monolith)

In a traditional Monolithic Agent approach, all tools (GA4, SEO, Database, CRM) are crammed into a single agent context.

**The Monolith Problem:**
1.  **Context Pollution**: The LLM gets confused by having too many tools in its prompt description.
2.  **Single Point of Failure**: A bug in the SEO tool crashes the web server for everyone.
3.  **Scaling Constraints**: You cannot scale the Analytics agent independently if it receives 90% of the traffic.

**The Microservice Solution (Our Approach):**
1.  **Cognitive Isolation**: The Analytics Agent *only* knows about GA4. It is an expert. The Orchestrator *only* knows who to call. This reduces hallucinations.
2.  **Independent Scaling**: We can deploy 10 replicas of the Analytics container and 1 of the SEO container based on load.
3.  **Fault Tolerance**: If the SEO service is down, the Orchestrator can still serve Analytics queries gracefully.
4.  **Team Velocity**: One team can work on the SEO logic (Port 8002) while another refactors the Orchestrator (Port 8080) without effectively stepping on each other's toes.

## 5. Project Structure

The codebase mirrors the architecture, enforcing separation of concerns.

```text
/
├── services/
│   ├── orchestrator/      # The Router
│   │   ├── main.py        # Public API (FastAPI)
│   │   └── agent.py       # Composition Logic (RemoteA2aAgent)
│   ├── analytics_agent/   # The GA4 Expert
│   │   ├── main.py        # A2A Server
│   │   ├── agent.py       # ADK Agent Definition
│   │   └── tools.py       # GA4 API Integration
│   └── seo_agent/         # The SEO Expert
│       ├── main.py        # A2A Server
│       ├── agent.py       # ADK Agent Definition
│       └── tools.py       # Pandas/Sheet Logic
├── shared/                # Common Utilities
│   └── llm.py             # Centralized Model Configuration
├── deploy.sh              # Unified Startup Script
└── requirements.txt       # Project Dependencies
```

## 6. How to Run

### Prerequisites
*   Python 3.10+
*   `credentials.json` (Google Service Account) in the root.

### Quick Start
We provide a unified deployment script that installs `uv`, creates a virtual environment, and launches all three microservices in the background.

```bash
bash deploy.sh
```

Once running:
*   **Orchestrator**: `http://localhost:8080` (Send POST requests here)
*   **Analytics Agent**: `http://localhost:8001` (Internal)
*   **SEO Agent**: `http://localhost:8002` (Internal)

### Example Query
```bash
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "How many active users did we have last week?",
           "propertyId": "123456"
         }'
```