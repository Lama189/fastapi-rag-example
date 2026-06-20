# rag-example

A RAG (Retrieval-Augmented Generation) API built with FastAPI, LangChain, pgvector, and Google Gemini. Upload PDF documents and ask questions about their content.

## How it works

```
Upload PDF → parse → chunk → embed (HuggingFace) → store in pgvector
Ask question → embed query → cosine similarity search → top-3 chunks → Gemini LLM → answer
```

- **PDF upload** — the file is parsed with PyMuPDF, split into overlapping text chunks, and each chunk is embedded with a HuggingFace sentence-transformer model running locally (CPU).
- **Embeddings storage** — chunks and their 1024-dim vectors are persisted in PostgreSQL with the pgvector extension. An HNSW index (vector_cosine_ops) is used for fast approximate nearest-neighbour search.
- **Question answering** — the query is embedded the same way, the 3 most similar chunks are retrieved, and the assembled context is sent to a Google Gemini LLM via a strict prompt that prevents hallucination outside the provided context.

## Stack

| Component | Technology |
|-----------|-----------|
| API | FastAPI |
| LLM | Google Gemini (gemini-3.5-flash) |
| Embeddings | BAAI/bge-m3 (HuggingFace, 1024 dims) |
| Vector DB | PostgreSQL + pgvector (HNSW index) |
| ORM | SQLAlchemy 2.0 async |
| Migrations | Alembic |
| Runtime | Python 3.12, uv |

## Prerequisites

- Docker + Docker Compose with the Compose plugin
- A Google API key for Gemini (set `GEMINI_LLM_API_KEY` in `.env`)

## Quick start

### 1. Clone and configure

```bash
git clone <repo-url>
cd rag-example
cp .env.example .env
# edit .env — set GEMINI_LLM_API_KEY
```

### 2. Start

```bash
docker compose up
```

This starts three services in order:

- **postgres** — PostgreSQL with pgvector, waits until healthy
- **migrations** — runs `alembic upgrade head`, then exits
- **web** — FastAPI on port 8000, waits for migrations to complete

## Configuration

Copy `.env.example` to `.env` and adjust:

```
APP__DB__HOST=postgres
APP__DB__NAME=rag_db
APP__DB__USER=postgres
APP__DB__PASSWORD=123

GEMINI_LLM_API_KEY=your-google-api-key
```

All `APP__` variables use `__` as the nested delimiter.

## API

Interactive docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

| Method | Path | Description |
|--------|------|-------------|
| POST | `/rag/upload/pdf` | Upload one or more PDFs and index them |
| GET | `/rag/ask-pdf?q=...` | Ask a question, returns plain text |

## Full cycle example

```bash
# 1. Configure
cp .env.example .env
# edit .env: set GEMINI_LLM_API_KEY

# 2. Start the app
docker compose up

# 3. Upload a PDF
curl -X POST http://localhost:8000/rag/upload/pdf \
  -F "files=@document.pdf"

# 4. Ask a question
curl "http://localhost:8000/rag/ask-pdf?q=What+is+the+document+about"
```
