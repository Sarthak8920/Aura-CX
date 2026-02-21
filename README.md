# Aura CX — Autonomous Commerce Agent Platform

**Enterprise-scale multi-agent AI system for retail and after-sales automation.**

Aura CX routes customer queries through specialized AI agents (intent, catalog, order, payment, policy, resolution) using LangGraph, then returns a single, policy-aware support response—suitable for payment issues, order delays, catalog questions, and refund/return eligibility.

---

## Features

- **Intent-based routing** — Classifies queries as `catalog`, `order`, `payment`, or `multiple` and runs only the relevant agents.
- **Specialized agents** — Catalog (alternatives), order status, payment status, policy checks, and a final resolution agent that synthesizes a reply.
- **Policy-aware responses** — Refund/return eligibility is checked against configurable rules before the final answer.
- **REST API** — FastAPI backend with `POST /chat` for integration with any frontend or service.
- **Demo UI** — Streamlit app for quick testing and demos.

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────────────────────────────┐
│   Client    │────▶│  FastAPI    │────▶│  LangGraph workflow (app.graph)           │
│ (Streamlit  │     │  /chat      │     │  intent → catalog | order | payment        │
│  or other)  │     │             │     │         → policy → resolve → final_answer │
└─────────────┘     └─────────────┘     └──────────────────────────────────────────┘
```

### Workflow steps

1. **Intent** — LLM classifies the customer query into `catalog`, `order`, `payment`, or `multiple`.
2. **Domain agents** (conditional):
   - **Catalog** — Suggests product alternatives (via `catalog_tools`).
   - **Order** — Fetches order status (via `order_tools`).
   - **Payment** — Fetches payment status (via `payment_tools`).
   - If intent is `multiple` or unknown, all three run in parallel.
3. **Policy** — Evaluates refund/return eligibility using `policy_tools` and previous agent outputs.
4. **Resolution** — LLM generates a single, professional support response from catalog, order, payment, and policy context.

State is carried through the graph via `AgentState` (query, intent, catalog_result, order_result, payment_result, policy_result, final_answer).

---

## Tech stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| LLM         | Groq (e.g. `llama-3.1-8b-instant`)  |
| Orchestration | LangChain, LangGraph               |
| Backend     | FastAPI, Uvicorn                    |
| UI (demo)   | Streamlit                           |
| Env         | python-dotenv                       |

---

## Project structure

```
aura-cx/
├── app/
│   ├── main.py              # FastAPI app, /chat endpoint
│   ├── graph.py             # LangGraph workflow definition
│   ├── schemas.py           # AgentState TypedDict
│   ├── llm.py               # Groq LLM client (uses GROQ_API_KEY)
│   ├── agents/
│   │   ├── intent_router.py  # Intent classification
│   │   ├── catalog_agent.py
│   │   ├── order_agent.py
│   │   ├── payment_agent.py
│   │   ├── policy_agent.py
│   │   └── resolution_agent.py
│   └── tools/
│       ├── catalog_tools.py
│       ├── order_tools.py
│       ├── payment_tools.py
│       └── policy_tools.py
├── ui.py                    # Streamlit demo UI
├── requirements.txt
├── .env                     # GROQ_API_KEY (create locally, do not commit)
└── README.md
```

---

## Prerequisites

- **Python** 3.10 or 3.11
- **Groq API key** — [Groq Console](https://console.groq.com/) (for LLM calls)

---

## Installation

1. **Clone and enter the project**

   ```bash
   cd aura-cx
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Do not commit `.env`; add it to `.gitignore` if using version control.

---

## Running the application

You need two processes: the FastAPI backend and (optionally) the Streamlit UI.

### 1. Start the backend (API)

From the project root:

```bash
uvicorn app.main:api --reload --host 0.0.0.0 --port 8000
```

- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### 2. Start the Streamlit UI (optional)

In a second terminal, from the project root:

```bash
streamlit run ui.py
```

- UI: `http://localhost:8501` (or the URL Streamlit prints).
- The UI sends requests to `http://127.0.0.1:8000/chat`; ensure the backend is running first.

### Production-style run (backend only)

For a production deployment, run the API without `--reload` and behind a reverse proxy (e.g. Nginx) or process manager (e.g. systemd, Docker):

```bash
uvicorn app.main:api --host 0.0.0.0 --port 8000 --workers 1
```

Adjust `--workers` and host/port as needed for your environment.

---

## API reference

### `GET /`

Health/info endpoint.

**Response example:**

```json
{
  "message": "Autonomous Commerce Agent Platform backend is running",
  "usage": {
    "chat": "POST /chat",
    "docs": "/docs"
  }
}
```

### `POST /chat`

Runs the multi-agent workflow and returns a single support-style response.

**Request body:**

```json
{
  "query": "My payment failed, money was deducted, order is delayed..."
}
```

**Response (200):**

```json
{
  "response": "Professional support response based on catalog, order, payment, and policy context."
}
```

**Note:** Each request uses a fresh state; no session is kept on the server.

---

## Environment variables

| Variable       | Required | Description                    |
|----------------|----------|--------------------------------|
| `GROQ_API_KEY` | Yes      | API key for Groq LLM (e.g. Llama). |

Loaded from `.env` via `python-dotenv` in `app/llm.py`.

---

## Extending the project

- **Tools** — Replace mock implementations in `app/tools/` with real APIs or DB calls (order service, payment gateway, catalog search).
- **Policy** — Extend `app/tools/policy_tools.py` (e.g. more rules, vector store, or external policy service).
- **Agents** — Add or change nodes in `app/graph.py` and implement new agents in `app/agents/`.
- **Intent** — Adjust the intent labels or add new intents in `app/agents/intent_router.py` and routing in `app/graph.py`.
- **LLM** — Change model or provider in `app/llm.py` (and add any new env vars to this README).

---

## License

Proprietary / All rights reserved (or add your chosen license).
