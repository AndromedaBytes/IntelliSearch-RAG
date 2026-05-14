# IntelliSearch V2

Cloud-Hybrid Multimodal Retrieval-Augmented Generation (RAG) Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.0-purple.svg)](https://www.trychroma.com/)

## What It Does

IntelliSearch V2 is a highly intelligent librarian that can see images, listen to audio, and read thousands of pages of text. It stores all knowledge in a local ChromaDB vector database and offloads cognitive reasoning to massive cloud models (GPT-4o + Llama 3.1 405B) via the GitHub Models free tier. Users get a packaged Windows .exe application with zero dependencies.

## Repository Layout

```
Project Xeno/
├── backend/            # FastAPI app, services, and routers
├── frontend/           # Next.js UI
├── scripts/            # Utility and verification scripts
├── tests/              # Pytest suite
├── run.py              # Local launcher for the backend
├── build_exe.py        # PyInstaller build entry point
└── .env.example        # Environment template for secrets
```

## Secrets And Environment

Copy [.env.example](.env.example) to `.env` and fill in your own values. Do not commit `.env`, GitHub token files, or any local key dumps.

Required settings:

- `GITHUB_TOKEN` or both `GITHUB_TOKEN_A` and `GITHUB_TOKEN_B`
- `CLIENT_KEY`

Optional settings:

- `NEXT_PUBLIC_CLIENT_KEY`
- `GITHUB_MODELS_BASE_URL`
- `CHROMA_PERSIST_DIR`
- `CHROMA_COLLECTION_NAME`
- `GPT4O_MODEL`
- `LLAMA_MODEL`

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  IntelliSearch V2 - Dual-Brain Architecture │
└─────────────────────────────────────────────┘

User Interface
    ↓
┌──────────────────────────────────────────────────────┐
│  Next.js Frontend (React + Tailwind + Framer Motion) │
└──────────────────────┬───────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  FastAPI Backend (Python 3.10+)                       │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌────────────────┐        ┌─────────────────────┐   │
│  │  Ingest Flow   │        │   Query Flow        │   │
│  ├────────────────┤        ├─────────────────────┤   │
│  │ GPT-4o         │        │ 1. ChromaDB Query   │   │
│  │ (Perception)   │        │ 2. Similarity Gate  │   │
│  │                │        │ 3. Llama 3.1 405B   │   │
│  │ - PDF Extract  │        │    (Logic Engine)   │   │
│  │ - Vision       │        │ 4. Citation Map     │   │
│  │ - Audio Trans  │        │ 5. Response + Cites │   │
│  └────────┬────────┘        └─────────────────────┘   │
│           ↓                                            │
│        ChromaDB (Local Persistent Store)              │
│        - Vector embeddings                            │
│        - Metadata + Citations                         │
│        - Similarity search (0.70 threshold)           │
└──────────────────────────────────────────────────────┘

GitHub Models (Free Tier)
├─ Token A → GPT-4o (Multimodal perception)
└─ Token B → Llama 3.1 405B (Reasoning, 128k context)
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- GitHub account (for free Models API tokens)

### Installation

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd intellisearch-v2
   ```

2. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your GitHub Models tokens and client key
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run server**
   ```bash
   python run.py
   ```

Server runs at `http://127.0.0.1:8000`

### Using the .exe

1. Download `IntelliSearch-V2.exe` from GitHub Releases
2. Double-click → First-run setup wizard appears
3. Enter GitHub Models tokens → App launches in browser

## API Reference

| Method | Endpoint | Auth | Body | Response |
|--------|----------|------|------|----------|
| GET | `/health` | None | - | `{status, corpus_size, models}` |
| POST | `/ingest` | Required | `file: binary` | `{status, chunks_stored}` |
| POST | `/query` | Required | `{query: str}` | `{answer, citations, gate_passed}` |

## Key Features

- **Dual-Brain Intelligence**: GPT-4o for perception, Llama 3.1 405B for reasoning
- **Multimodal Ingestion**: PDF, Images, Audio → semantic text
- **Similarity Gate**: 0.70 cosine threshold blocks hallucinations
- **Deep Citations**: Every answer links to source documents
- **Zero Local GPU**: Cloud inference on any hardware
- **Privacy First**: Embeddings stay local
- **Single .exe**: No Python installation required

## Development

### Run tests
```bash
pytest tests/ -v --asyncio-mode=auto
```

### Verify GitHub Models Token (Foundry SDK)
```bash
python scripts/verify_foundry_inference.py
```

PowerShell example:
```powershell
$Env:GITHUB_TOKEN="YOUR-GITHUB-TOKEN-GOES-HERE"
python scripts/verify_foundry_inference.py
```

### Build frontend
```bash
cd frontend
npm install
npm run build
```

### Build Windows EXE
```bash
python build_exe.py
```

### Run locally
```bash
python run.py
```

### Docker deployment
```bash
docker-compose -f docker-compose.prod.yml up
```

## How to Get GitHub Models Tokens

1. Visit [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Create Personal Access Token with `models:read` permission
3. Set `GITHUB_TOKEN` in `.env` (or use `GITHUB_TOKEN_A` and `GITHUB_TOKEN_B`)
4. Paste into `.env` file

## Architecture Deep Dive

### Similarity Gate (Anti-Hallucination)
- Retrieves top-15 chunks from ChromaDB
- If top similarity < 0.70 cosine: blocks LLM call
- Returns: "Information not found" message
- Users can't be misled by LLM reasoning on weak context

### Citation Mapping
- Each answer chunk tagged with source metadata
- Format: `[Source: filename.pdf]`
- Users verify information independently

### Chunking Strategy
- Chunk size: 512 characters (overlap: 64)
- Preserves document structure
- Metadata includes page/section info

## Project Structure

```
intellisearch-v2/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── config.py        # Settings & env vars
│   │   ├── security.py      # Client key auth
│   │   ├── models.py        # Pydantic models
│   │   ├── routers/
│   │   │   ├── ingest.py    # POST /ingest
│   │   │   └── query.py     # POST /query
│   │   └── services/
│   │       ├── chromadb_service.py
│   │       ├── gpt4o_service.py
│   │       └── llama_service.py
├── frontend/              # Next.js React SPA
├── tests/                 # pytest suite
├── run.py                 # Process launcher
└── build_exe.py           # PyInstaller script
```

## Performance Targets

- Query latency: < 5 seconds (ChromaDB search < 500ms, Llama inference < 4.5s)
- Ingest latency: < 10 seconds per file (depends on file size & GPU availability)
- Corpus size: tested up to 10k documents

## Security

- **X-IntelliSearch-Client-Key** header required on `/ingest` and `/query`
- Timing-safe comparison prevents key enumeration attacks
- CORS restricted by default
- No API key logging
- Secrets stay in `.env` and are excluded from git

## License

MIT License - see LICENSE file

---

**Built for MakersGroup** | GPT-4o · Llama 3.1 405B · ChromaDB · FastAPI · PyInstaller
