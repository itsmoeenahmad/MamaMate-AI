# MamaMate AI – For Women's Health Assistant

This is the backend codebase for **MamaMate**, an AI-powered assistant for women. It uses **LangChain**, **OpenAI**, **FastAPI**, **ChromaDB**, and **MongoDB** to deliver intelligent, context-aware support in gynecology, sex education, mental wellness, and motherhood.

---

## Tech Stack

| Component        | Tool Used           | Purpose                         |
|------------------|---------------------|----------------------------------|
| LLM              | OpenAI              | Language understanding + reasoning |
| Framework        | LangChain           | Agentic AI + RAG capabilities    |
| API Server       | FastAPI             | REST API for frontend            |
| Vector DB        | ChromaDB            | Document embeddings & retrieval (RAG) |
| Memory Store     | MongoDB             | Long-term conversational memory  |

---

## Features

- **Agentic RAG System** using LangChain
  - Retrieves answers from uploaded books/resources
  - Agent uses OpenAI Tool Calling to decide and execute multi-step tasks
- **Memory Integration**
  - MongoDB-based memory stores chat history and context
- **Tool Calling (OpenAI)**
  - Custom AI agents execute multi-step tasks
- **FastAPI Endpoints**
  - Clean RESTful API to connect with the frontend (mobile or web)

---

**Before You Use the Code**

Take a moment to read through the code instead of just copy-pasting it. I have added comments to explain each part so you can understand what is happening step by step.

If anything is unclear or you are stuck, feel free to reach out - you can DM me on Instagram or LinkedIn. I am happy to help!
