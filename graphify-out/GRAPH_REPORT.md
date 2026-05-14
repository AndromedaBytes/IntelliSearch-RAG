# Graph Report - .  (2026-05-05)

## Corpus Check
- Corpus is ~23,474 words - fits in a single context window. You may not need a graph.

## Summary
- 333 nodes · 334 edges · 50 communities (47 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Audio Transcription Service|Audio Transcription Service]]
- [[_COMMUNITY_Citation|Citation]]
- [[_COMMUNITY_handleFileSelected()|handleFileSelected()]]
- [[_COMMUNITY_chromadb_service.py|chromadb_service.py]]
- [[_COMMUNITY_test_ingest.py|test_ingest.py]]
- [[_COMMUNITY_create_minimal_pdf()|create_minimal_pdf()]]
- [[_COMMUNITY_Chat Canvas Interface Component|Chat Canvas Interface Component]]
- [[_COMMUNITY_auth_error_handler()|auth_error_handler()]]
- [[_COMMUNITY_gpt4o_service.py|gpt4o_service.py]]
- [[_COMMUNITY_main()|main()]]
- [[_COMMUNITY_check_backend_health()|check_backend_health()]]
- [[_COMMUNITY_Doctor|Doctor]]
- [[_COMMUNITY_Allow either one shared token or separate model tokens.|Allow either one shared token or separate model tokens.]]
- [[_COMMUNITY_llama_service.py|llama_service.py]]
- [[_COMMUNITY_conftest.py|conftest.py]]
- [[_COMMUNITY_test_query.py|test_query.py]]
- [[_COMMUNITY_entry.py|entry.py]]
- [[_COMMUNITY_kill_ghost_processes()|kill_ghost_processes()]]
- [[_COMMUNITY_build_exe.py|build_exe.py]]
- [[_COMMUNITY_MessageBubble()|MessageBubble()]]
- [[_COMMUNITY_ask_model()|ask_model()]]
- [[_COMMUNITY_convert_to_icon()|convert_to_icon()]]
- [[_COMMUNITY_main()|main()]]
- [[_COMMUNITY_create_dragon_icon.py|create_dragon_icon.py]]
- [[_COMMUNITY_Verify client key from request header using timing-safe comparison.     If no h|Verify client key from request header using timing-safe comparison.     If no h]]

## God Nodes (most connected - your core abstractions)
1. `ChromaDBService` - 12 edges
2. `IntelliSearch V2 Platform` - 9 edges
3. `FastAPI Backend` - 8 edges
4. `Next.js Frontend` - 8 edges
5. `GPT4oService` - 6 edges
6. `main()` - 6 edges
7. `SetupWindow` - 5 edges
8. `DeleteResponse` - 5 edges
9. `getHeaders()` - 5 edges
10. `Doctor` - 5 edges

## Surprising Connections (you probably didn't know these)
- `IntelliSearch V2 Platform` --implements--> `Next.js Frontend`  [EXTRACTED]
  PROJECT_SUMMARY.md → README.md
- `IntelliSearch V2 Platform` --uses--> `Release Checklist Process`  [EXTRACTED]
  PROJECT_SUMMARY.md → RELEASE_CHECKLIST.md
- `FastAPI Backend` --conceptually_related_to--> `Unit Tests (pytest + httpx async)`  [EXTRACTED]
  README.md → PROJECT_SUMMARY.md
- `Docker Compose Production Orchestration` --orchestrates--> `FastAPI Backend`  [EXTRACTED]
  docker-compose.prod.yml → README.md
- `Next.js Frontend` --implements--> `Dark Theme UI with Glassmorphism`  [EXTRACTED]
  README.md → PROJECT_SUMMARY.md

## Hyperedges (group relationships)
- **RAG Pipeline Core Workflow** — gpt4o_perception_engine, chromadb_vector_database, llama_405b_logic_engine, similarity_gate_antihallu [EXTRACTED 1.00]
- **Frontend UI Component System** — nextjs_frontend, tailwind_css_framework, framer_motion_animation, dark_theme_ui [EXTRACTED 1.00]
- **CSS Build and Processing Pipeline** — globals_css_entry, postcss_processor, tailwind_css_framework, postcss_config_mjs [EXTRACTED 1.00]
- **API Security and Authentication** — client_key_authentication, cors_middleware, ingest_endpoint, query_endpoint [INFERRED 0.85]
- **Windows EXE Distribution Pipeline** — pyinstaller_distribution, windows_exe_distribution, setup_window_tkinter, first_run_user_experience, github_actions_cicd [EXTRACTED 1.00]
- **Multimodal File Ingestion System** — ingest_flow_workflow, pdf_extraction_service, audio_transcription_service, image_extraction_service, gpt4o_perception_engine [EXTRACTED 1.00]
- **Containerization and Orchestration** — dockerfile_containerization, docker_compose_prod, fastapi_backend, chromadb_vector_database [EXTRACTED 1.00]
- **Testing and Quality Validation** — unit_tests_pytest, integration_tests_suite, release_checklist_process, build_guide_documentation [INFERRED 0.80]

## Communities (50 total, 3 thin omitted)

### Community 0 - "Audio Transcription Service"
Cohesion: 0.06
Nodes (37): Audio Transcription Service, Build Guide Documentation, ChromaDB Vector Database, Text Chunking Strategy (512 chars, 64 overlap), Citation Mapping System, Client Key Authentication (X-IntelliSearch-Client-Key), CORS Middleware, Docker Compose Production Orchestration (+29 more)

### Community 1 - "Citation"
Cohesion: 0.09
Nodes (29): Citation, CorpusFile, CorpusInfo, DeleteResponse, HealthResponse, IngestResponse, QueryRequest, QueryResponse (+21 more)

### Community 2 - "handleFileSelected()"
Cohesion: 0.12
Nodes (15): handleFileSelected(), handleClearCorpus(), handleDeleteFile(), loadCorpus(), Sidebar(), ToastNotification(), useChat(), useHealth() (+7 more)

### Community 3 - "chromadb_service.py"
Cohesion: 0.09
Nodes (13): ChromaDBService, ChromaDB Service - Vector database layer for IntelliSearch V2 Handles local per, Query corpus and return top-k most similar chunks.                  Args:, Service for managing ChromaDB vector database operations, Get total number of documents in corpus, Initialize ChromaDB persistent client and collection, Delete all chunks from a specific source.                  Args:, Get list of all unique sources (files) in corpus with metadata. (+5 more)

### Community 4 - "test_ingest.py"
Cohesion: 0.09
Nodes (21): Ingest endpoint tests for IntelliSearch V2, Test query over 2000 chars returns 400, Test query on empty corpus returns gate_blocked response, Test GET /health endpoint, Test ingest without client key returns 403, Test ingest with invalid client key returns 403, Test ingest with unsupported file type returns 415, Short audio transcripts should still become searchable corpus chunks. (+13 more)

### Community 5 - "create_minimal_pdf()"
Cohesion: 0.12
Nodes (17): create_minimal_pdf(), create_minimal_png(), Integration test script for IntelliSearch V2 Tests the complete end-to-end syst, Test 3: Ingest PDF file, Test 4: Query gate blocks on empty/low-context corpus, Test 5: Citation format validation, Run all integration tests, Create minimal valid PDF for testing (+9 more)

### Community 6 - "Chat Canvas Interface Component"
Cohesion: 0.13
Nodes (16): Chat Canvas Interface Component, Citation Pills Component, Dark Theme UI with Glassmorphism, Drag-Drop File Upload Component, Framer Motion Animation Library, globals.css TailwindCSS Entry Point, Markdown Rendering in Chat, Next.js Frontend (+8 more)

### Community 7 - "auth_error_handler()"
Cohesion: 0.17
Nodes (11): auth_error_handler(), general_exception_handler(), health_check(), lifespan(), rate_limit_handler(), IntelliSearch V2 - FastAPI main application Dual-Brain Cloud-Hybrid Multimodal, Application lifecycle manager, Handle OpenAI rate limit errors (+3 more)

### Community 8 - "gpt4o_service.py"
Cohesion: 0.18
Nodes (7): GPT4oService, GPT-4o Perception Engine - Multimodal ingestion service Converts images, audio,, Extract audio content via transcription.         Uses GPT-4o text analysis on m, Extract text from PDF with vision fallback for scanned pages., Service for multimodal content extraction using GPT-4o, Initialize async OpenAI client for GPT-4o, Extract semantic text from image using GPT-4o vision.                  Args:

### Community 9 - "main()"
Cohesion: 0.22
Nodes (6): main(), First-run setup window for IntelliSearch V2 .exe Collects GitHub tokens and cli, Generate a random client key, Save configuration to .env file, Check if .env exists, show setup if not, SetupWindow

### Community 10 - "check_backend_health()"
Cohesion: 0.29
Nodes (9): check_backend_health(), check_github_models_auth(), check_query_endpoint(), main(), print_result(), Run all health checks, Check /health endpoint, Check GitHub Models authentication using Foundry SDK (+1 more)

### Community 11 - "Doctor"
Cohesion: 0.28
Nodes (4): Doctor, Doctor script for IntelliSearch V2 system diagnostics Validates environment, de, Record a check result, Run all diagnostic checks

### Community 12 - "Allow either one shared token or separate model tokens."
Cohesion: 0.25
Nodes (6): Allow either one shared token or separate model tokens., Find a usable .env file in source or packaged layouts., Application Configuration, _resolve_env_file(), Settings, BaseSettings

### Community 13 - "llama_service.py"
Cohesion: 0.25
Nodes (5): LlamaService, Llama 3.1 405B Logic Engine - Reasoning and synthesis service Uses 128k context, Service for reasoning and synthesis using Llama 3.1 405B, Initialize async OpenAI client for Llama 3.1 405B, Synthesize an answer from context chunks using Llama 3.1 405B.

### Community 14 - "conftest.py"
Cohesion: 0.25
Nodes (7): Pytest configuration and fixtures for IntelliSearch V2 tests, Get valid client key from environment, Create minimal valid PDF bytes for testing, Create minimal valid PNG bytes for testing, sample_pdf_bytes(), sample_png_bytes(), valid_client_key()

### Community 15 - "test_query.py"
Cohesion: 0.25
Nodes (7): Query endpoint tests for IntelliSearch V2, Test query response has required fields, Test citation objects have required fields, Test similarity gate blocks low-confidence queries, test_citation_structure(), test_query_response_structure(), test_similarity_gate_logic()

### Community 16 - "entry.py"
Cohesion: 0.33
Nodes (6): check_port_available(), main(), IntelliSearch V2 - Windows .exe Entry Point Starts FastAPI backend and serves N, Poll until port is ready, Start FastAPI backend, run_backend()

### Community 17 - "kill_ghost_processes()"
Cohesion: 0.38
Nodes (6): kill_ghost_processes(), main(), Process orchestration launcher for IntelliSearch V2. Manages ghost process clea, Kill any existing processes listening on the specified port., Poll socket until server accepts connections., wait_for_server()

### Community 18 - "build_exe.py"
Cohesion: 0.5
Nodes (4): main(), PyInstaller build script for IntelliSearch V2 Windows .exe Bundles backend (Fas, Run shell command and return success status, run_command()

### Community 21 - "ask_model()"
Cohesion: 0.6
Nodes (4): ask_model(), main(), Ask the same question to two models (GitHub Models + Llama) via Foundry SDK  U, resolve_token()

### Community 22 - "convert_to_icon()"
Cohesion: 0.67
Nodes (3): convert_to_icon(), main(), Convert image to multi-resolution ICO file

### Community 23 - "main()"
Cohesion: 0.67
Nodes (3): main(), Verify GitHub Models auth using Microsoft Foundry Inference SDK.  Usage (Power, _resolve_token()

## Knowledge Gaps
- **125 isolated node(s):** `PyInstaller build script for IntelliSearch V2 Windows .exe Bundles backend (Fas`, `Run shell command and return success status`, `Create a simple dragon shield icon`, `IntelliSearch V2 - Windows .exe Entry Point Starts FastAPI backend and serves N`, `Poll until port is ready` (+120 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IntelliSearch V2 Platform` connect `Audio Transcription Service` to `Chat Canvas Interface Component`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `Next.js Frontend` connect `Chat Canvas Interface Component` to `Audio Transcription Service`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `PyInstaller build script for IntelliSearch V2 Windows .exe Bundles backend (Fas`, `Run shell command and return success status`, `Create a simple dragon shield icon` to the rest of the system?**
  _125 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Audio Transcription Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._
- **Should `Citation` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `handleFileSelected()` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `chromadb_service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._