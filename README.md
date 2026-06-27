# InterTraceAI

> A privacy-first, local AI assistant for personal document retrieval — no cloud, no subscriptions, no data leaving your machine.

InterTraceAI is a multiplatform desktop application that lets you index your personal PDF documents and query them in natural language. All processing happens entirely on your local hardware: document ingestion, semantic search, and language model inference run without any internet connection or external API calls.

---

## How it works

InterTraceAI implements a **RAG (Retrieval-Augmented Generation)** pipeline:

1. **Ingest** — the app scans your `~/Documents` folder for PDF files, extracts their text, splits it into semantic chunks, generates vector embeddings, and stores everything in a hybrid persistence layer (SQLite for metadata, ChromaDB for vectors).
2. **Retrieve** — when you ask a question, the same embedding model encodes your query and ChromaDB finds the most semantically similar chunks from your indexed documents.
3. **Generate** — the retrieved chunks are assembled into a context-aware prompt and sent to a local language model (via LM Studio), which produces a grounded answer citing the source documents.

---

## Features

- 🔒 **100% local** — no data ever leaves your machine
- 📄 **PDF ingestion** with automatic text extraction and semantic chunking
- 🔍 **Semantic search** using `all-MiniLM-L6-v2` embeddings
- 💬 **Natural language chat** interface with source attribution per response
- 📂 **Document index browser** with ingestion date and file path
- 🔄 **Full re-ingestion** with a single button (resets and rebuilds the entire index)
- 🖥️ **Multiplatform** desktop app (Windows, macOS, Linux) built with Flutter
- ⚙️ **Single configuration file** — tune chunking, model, token budget, search depth, and more from one place

---

## Architecture

The system follows a **local client-server architecture**:

```
Flutter Desktop (frontend)
        │  HTTP / REST
        ▼
FastAPI Backend (Python)
   ├── Search Engine  →  scans ~/Documents for PDFs
   ├── Ingest Pipeline  →  extract → chunk → embed → store
   ├── RAG Pipeline  →  retrieve → build context → generate
   └── Data Layer
        ├── SQLite (via SQLModel)  →  document & chunk metadata
        └── ChromaDB  →  vector embeddings

LM Studio (separate process)  →  local LLM inference
```

The backend exposes three endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/documents` | List all indexed documents |
| `POST` | `/ingest/reset` | Reset index and re-ingest all documents |
| `POST` | `/query` | Submit a natural language query |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Flutter 3 + Dart, Riverpod, GoRouter |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` |
| Vector store | ChromaDB (persistent, in-process) |
| Relational DB | SQLite via SQLModel |
| Document loading | LangChain Community — PyMuPDFLoader |
| Text splitting | LangChain — RecursiveCharacterTextSplitter |
| LLM inference | LM Studio (OpenAI-compatible local endpoint) |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Flutter 3.x (with desktop support enabled)
- [LM Studio](https://lmstudio.ai/) with a model loaded and the local server running on `http://localhost:1234`

### Backend

```bash
cd backend
pip install -r requirements.txt
./run.sh        # starts uvicorn on http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend
flutter pub get
flutter run -d <your-desktop-target>
```

### Usage

1. Place PDF files in your `~/Documents` folder.
2. Open the app and navigate to the **Info** screen.
3. Press **Ingest** to index your documents.
4. Switch to the **Chat** screen and start asking questions.

---

## Configuration

All system parameters live in `backend/app/core/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model for embeddings |
| `LLM_MODEL` | `google/gemma-3-1b` | Model name sent to LM Studio |
| `CHUNK_SIZE` | `1500` | Max characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between consecutive chunks |
| `TOP_K` | `3` | Number of chunks retrieved per query |
| `MAX_CONTEXT_TOKENS` | `1200` | Token budget for the RAG context window |
| `DISTANCE_THRESHOLD` | `1.0` | Max cosine distance to accept a retrieved chunk |
| `MAX_DOCUMENTS` | `10` | Maximum number of documents to index |
| `MAX_PDF_SIZE_MB` | `10` | Maximum size of a single PDF |
| `SEARCH_MAX_DEPTH` | `3` | Directory recursion depth when scanning |
| `TEMPERATURE` | `0.1` | LLM generation temperature |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (endpoints.py)
│   │   ├── core/         # config.py — single source of truth
│   │   ├── db/           # models, session, repository, chromadb
│   │   ├── services/
│   │   │   ├── rag/      # pipeline, ingest, retriever, generator
│   │   │   └── search/   # filesystem search engine
│   │   └── main.py
│   ├── requirements.txt
│   └── run.sh
└── frontend/
    └── lib/
        ├── core/          # router, theme, colors
        ├── features/
        │   ├── chat/      # chat screen, controller, repository, model
        │   ├── doc/       # docs screen, controller, repository, model
        │   └── info/      # info screen, ingest controller & repository
        └── shared/        # layout, sidebar, providers
```

---

## Screenshots

<img width="1372" height="807" alt="Captura de pantalla 2026-05-23 190404" src="https://github.com/user-attachments/assets/6c066e0a-3e7f-4121-88ba-3dd88c138faf" />
<img width="1372" height="809" alt="Captura de pantalla 2026-05-23 181253" src="https://github.com/user-attachments/assets/b77ff731-46e3-4f07-b8ab-2f78542171f4" />
<img width="1261" height="707" alt="Captura de pantalla 2026-05-23 180347" src="https://github.com/user-attachments/assets/0fdd0eff-513b-49e8-8100-21341fe5b65e" />

---

## Limitations

- Only **PDF** files are currently supported
- No **conversational memory** — each query is independent
- Designed for **single-user**, local use only (no auth, no multi-user)
- Performance depends entirely on local hardware

---

## Future Work

- Response **streaming via WebSocket** for real-time output
- Support for additional formats: `.docx`, `.txt`, `.md`, `.csv`
- Individual file selection and removal from the index
- Automatic re-ingestion on filesystem changes
- Embedded inference via `llama-cpp-python` (no LM Studio dependency)
- Conversation history in the RAG prompt

---

## Author

**Ángel Sáez Rosique**  
Bachelor's Thesis — Computer Engineering  
Universidad de Murcia, May 2026
