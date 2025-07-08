# MamaMate AI – LangChain Backend for Women's Health Assistant

This is the backend codebase for **MamaMate**, an AI-powered assistant for women. It uses **LangChain**, **OpenAI**, **FastAPI**, **ChromaDB**, and **MongoDB** to deliver intelligent, context-aware support in gynecology, sex education, mental wellness, and motherhood.

---

## ⚙️ Tech Stack

| Component        | Tool Used           | Purpose                         |
|------------------|---------------------|----------------------------------|
| LLM              | OpenAI              | Language understanding + reasoning |
| Framework        | LangChain           | Agentic AI + RAG capabilities    |
| API Server       | FastAPI             | REST API for frontend            |
| Vector DB        | ChromaDB            | Document embeddings & retrieval (RAG) |
| Memory Store     | MongoDB             | Long-term conversational memory  |

---

## 🧠 Features

- 🔍 **Agentic RAG System** using LangChain
  - Retrieves answers from uploaded books/resources
  - Agent follows ReAct-style reasoning
- 🧠 **Memory Integration**
  - MongoDB-based memory stores chat history and context
- 📂 **Tool Calling (OpenAI)**
  - Custom AI agents execute multi-step tasks
- 🔌 **FastAPI Endpoints**
  - Clean RESTful API to connect with the frontend (mobile or web)

---

## 📁 Project Structure

```bash
mamamate-ai-backend/
├── api/                     # FastAPI route handlers
│   ├── chat.py              # Main chat endpoint
│   └── auth.py              # Optional: Auth routes if used
├── agents/                  # LangChain agent setup
│   └── custom_agent.py
├── rag/                     # RAG system (Chroma setup, documents)
│   ├── retriever.py
│   └── ingest_docs.py
├── memory/                  # MongoDB memory handler
│   └── memory_manager.py
├── tools/                   # Optional custom tools
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
└── README.md
