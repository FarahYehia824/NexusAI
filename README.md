# 🤖 NexusAI — Enterprise AI Assistant

An intelligent AI assistant that dynamically routes user questions between company documents (RAG) and structured business data (SQL), built with a LangGraph-orchestrated multi-agent architecture.

🎥 **Demo Video:** [https://drive.google.com/your-link](https://drive.google.com/drive/folders/1dfRo_Cs0Y9Wqg_IOZu3wGdOJxQtF2lDf?hl=ar)

> Built as a hands-on project to demonstrate practical Agentic AI engineering: tool calling, routing, multi-step orchestration, and RAG — the core skills required for production AI Engineering roles.

---

## 🎯 What It Does

NexusAI answers natural language questions by automatically deciding whether to search company policy documents or query a structured database — no manual source selection needed.

```
👤 "What is the maternity leave policy?"     → routed to RAG  (company documents)
👤 "Which employee has the highest salary?"  → routed to SQL  (structured database)
```

---

## 🏗️ Architecture

```
                    User
                     │
               Streamlit UI
                     │
              FastAPI (/chat)
                     │
            LangGraph Agent (StateGraph)
                     │
              ┌──────┴───────┐
              │              │
         Router Node    Response Generator
              │              │
       ┌──────┴──────┐       │
       │             │       │
   RAG Agent     SQL Agent   │
       │             │       │
  FAISS + PDFs   SQLite      │
       │             │       │
       └──────┬──────┘       │
              │               
          Groq LLM  ──────────
       (openai/gpt-oss-120b)
```

**Flow:** every question enters the graph at the **Router Node**, which classifies it as `documents` or `database`. Based on that decision, the graph routes to either the **RAG Agent** (semantic search over company PDFs via FAISS) or the **SQL Agent** (natural language → SQL → SQLite execution). Both paths converge on a dedicated **Response Generator Node**, which produces a single, consistently formatted final answer — making it easy to add new agents (e.g. Email Agent, Analytics Agent) without touching the rest of the pipeline.

---

## ✨ Features

- **Dynamic tool routing** — automatically selects RAG or SQL based on question intent, no manual switching
- **RAG over enterprise documents** — semantic search across company policy PDFs using Sentence-Transformers + FAISS
- **Natural language to SQL** — converts plain English questions into executable SQL queries
- **LangGraph orchestration** — a StateGraph with dedicated nodes (Router → Agent → Response Generator) instead of hardcoded if/else logic
- **Evaluation layer** — logs latency and groundedness for every response
- **Full-stack delivery** — FastAPI backend + Streamlit chat UI, fully working end-to-end

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (`openai/gpt-oss-120b`) |
| Orchestration | LangGraph, LangChain |
| RAG | Sentence-Transformers, FAISS, pypdf |
| Structured Data | SQLite |
| API | FastAPI, Pydantic, Uvicorn |
| UI | Streamlit |
| Language | Python 3.10 |

---

## 📂 Project Structure

```
nexusai/
├── agents/
│   ├── router.py          # LangGraph StateGraph: Router, SQL, RAG, Response Generator nodes
│   ├── rag_agent.py        # RAG: retrieval + answer generation over PDFs
│   └── sql_agent.py        # Text-to-SQL agent
├── services/
│   ├── llm_service.py      # Single point of contact with the Groq API
│   ├── embedding_service.py # PDF chunking, embeddings, FAISS index + search
│   └── database_service.py # SQLite table setup and query execution
├── models/
│   └── schemas.py          # Pydantic request/response models
├── config/
│   ├── settings.py         # Loads environment variables
│   └── .env                # API keys (not committed)
├── database/                # SQLite database file
├── documents/                # Company policy PDFs (source for RAG)
├── vector_store/             # FAISS index + chunk metadata
├── backend/
│   └── main.py               # FastAPI app and /chat endpoint
├── frontend/
│   └── app.py                 # Streamlit chat UI
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
git clone https://github.com/<your-username>/nexusai.git
cd nexusai

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create `config/.env` and add your API key:
```
GROQ_API_KEY=your_key_here
```

### Running the app

Terminal 1 — start the backend:
```bash
uvicorn backend.main:app --reload
```

Terminal 2 — start the frontend:
```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501` and start chatting.

API docs (Swagger UI) are available at `http://127.0.0.1:8000/docs`.

---

## 📊 Evaluation

Every response is logged with:
- **Latency** — end-to-end response time in seconds
- **Source used** — which agent (RAG or SQL) handled the question
- **Groundedness** — whether the final answer was generated from an actual retrieved/queried result, rather than the model's own knowledge

---

## 🗺️ Roadmap

- **v1.1** — Docker containerization + deployment
- **v1.2** — Conversation memory across turns
- **v1.3** — Multi-tab UI (Chat / Upload PDF / SQL Dashboard / Logs)
- **v1.4** — True multi-agent supervisor architecture
- **v2.0** — MCP integration, Microsoft Teams, Azure deployment

---

## 📝 License

This is a personal learning/portfolio project.
