# IntelliSupport — Project Report

## 1. Project Overview

**IntelliSupport** is a production-grade autonomous customer support RAG (Retrieval-Augmented Generation) platform for **Nexora**, a fictional B2B project management SaaS company. It ingests support documentation, classifies user intents, retrieves relevant context via hybrid search, and generates grounded responses using an LLM.

### Architecture
```
User Query → IntentClassifier → Embedder → HybridRetriever → PromptBuilder → ResponseGenerator → Response
                                           ├─ VectorStore (pgvector)
                                           └─ BM25Retriever (rank_bm25)
```

---

## 2. Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.12 |
| LLM Provider | OpenAI (`gpt-4o-mini`, `text-embedding-3-small`) or NVIDIA (`meta/llama-3.1-8b-instruct`, `nvidia/nv-embedqa-e5-v5`) |
| Vector DB | PostgreSQL 16 + pgvector |
| Keyword Search | BM25 via `rank_bm25` |
| API Framework | FastAPI (port 8001) |
| DB Client | psycopg2 (raw SQL, no ORM) |
| Validation | Pydantic v2 |
| Testing | pytest (23 tests) |
| Frontend | Streamlit (port 8501) |
| Container | Docker (`pgvector/pgvector:pg16`) |

---

## 3. Directory Structure

```
intellisupport/
├── ingestion/          # Document loading, chunking, embedding
│   ├── loader.py       # DocumentLoader, Document model
│   ├── chunker.py      # DocumentChunker, Chunk model
│   ├── embedder.py     # Embedder with OpenAI/NVIDIA dual support
│   └── seed_data.py    # 10 Nexora support documents
├── retrieval/          # Dense + sparse hybrid search
│   ├── vector_store.py # pgvector cosine similarity search
│   ├── bm25_retriever.py   # BM25Okapi keyword search
│   └── hybrid_retriever.py # Alpha-weighted merge + Jaccard reranking
├── generation/         # Prompt construction + LLM response
│   ├── prompt_builder.py   # RAG + clarification prompts
│   └── response_generator.py # LLM call with fallback
├── classification/     # Intent classification
│   └── intent_classifier.py # 7 intents via LLM JSON mode
├── evaluation/         # LLM-as-a-judge metrics
│   ├── faithfulness.py # Claim extraction & verification
│   ├── relevance.py    # Chunk relevance scoring (0/1/2)
│   └── evaluator.py    # PipelineEvaluator + BenchmarkReport
├── feedback/           # User feedback loop
│   └── feedback_store.py # Store, summary, low-rated queries
├── api/                # FastAPI REST endpoints
│   ├── main.py         # 5 endpoints: /query, /evaluate, /feedback, /summary, /health
│   └── schemas.py      # Pydantic request/response models
├── database/
│   └── migrations/
│       └── 001_initial.sql  # Schema: VECTOR(1536) for submission
├── tests/              # 23 pytest tests
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_generation.py
│   └── test_evaluation.py
├── config.py           # Settings via pydantic-settings
├── .env.example        # Both OpenAI and NVIDIA templates
├── requirements.txt
├── README.md
├── report.md           # This file
└── app.py              # Streamlit frontend
```

---

## 4. Database Schema

Schema: `intellisupport` (PostgreSQL + pgvector)

### Tables

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `documents` | doc_id (PK), title, content, source_url, metadata | Raw support docs |
| `chunks` | chunk_id (PK), doc_id (FK), content, embedding VECTOR(1536/1024) | Semantic search index |
| `queries` | query_id (PK), raw_query, intent, intent_confidence | Incoming query log |
| `responses` | response_id (PK), query_id (FK), response_text, retrieved_chunk_ids[], faithfulness_score, relevance_score | Generated response log |
| `feedback` | feedback_id (PK), response_id (FK), rating (1-5), comment | User ratings |

### Dimension Note
- **OpenAI** (`text-embedding-3-small`): 1536-dim → `VECTOR(1536)`
- **NVIDIA** (`nv-embedqa-e5-v5`): 1024-dim → `VECTOR(1024)`
- Migration file defaults to `VECTOR(1536)` per spec. Change to `VECTOR(1024)` for NVIDIA.

---

## 5. Core Components

### 5.1 Ingestion Pipeline
- **DocumentLoader**: Validates `doc_id` pattern `^doc_\d{3}$`, rejects empty content, upserts to DB
- **DocumentChunker**: Sliding window with configurable `chunk_size` and `chunk_overlap`, whitespace tokenization
- **Embedder**: OpenAI/NVIDIA auto-detection, 3-retry exponential backoff, batch embedding, stores with pgvector

### 5.2 Retrieval System
- **VectorStore**: Cosine similarity via `<=>` operator, with threshold filtering
- **BM25Retriever**: In-memory index via `BM25Okapi`, normalization to [0,1], `rebuild_index()`
- **HybridRetriever**: `final_score = alpha * vector + (1-alpha) * bm25`, dedup, Jaccard reranking

### 5.3 Classification
- **IntentClassifier**: 7 labels (`billing`, `technical_issue`, `feature_request`, `integration`, `account_management`, `data_and_export`, `general_inquiry`), JSON mode, graceful fallback

### 5.4 Generation
- **PromptBuilder**: Anti-hallucination system prompt, chunk citations, clarification prompt for empty context
- **ResponseGenerator**: LLM call with fallback (retries if <20 chars or "I don't know")

### 5.5 Evaluation (LLM-as-a-Judge)
- **FaithfulnessEvaluator**: Extracts claims, checks against context, returns `supported/total` ratio
- **RelevanceEvaluator**: Scores each chunk 0/1/2, normalizes to [0,1]
- **PipelineEvaluator**: End-to-end benchmark with `retrieval_hit_rate`, `intent_accuracy`, `avg_faithfulness`, `avg_relevance`

### 5.6 API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | `/query` | Classify, retrieve, generate, save |
| POST | `/evaluate/{response_id}` | Faithfulness + relevance scores |
| POST | `/feedback` | Store user rating (1-5) |
| GET | `/feedback/summary/{response_id}` | Average rating + count |
| GET | `/health` | DB status + chunk count |

---

## 6. Seed Documents (10 Nexora Docs)

| doc_id | Title | Category |
|--------|-------|----------|
| doc_001 | Getting Started with Nexora | Onboarding |
| doc_002 | Managing Team Members and Permissions | Administration |
| doc_003 | Billing and Subscription Plans | Billing |
| doc_004 | Integrations: Slack, GitHub, and Jira | Integrations |
| doc_005 | Project Templates and Workflows | Workflows |
| doc_006 | Notifications and Alert Settings | Account |
| doc_007 | Data Export and Backup | Administration |
| doc_008 | Two-Factor Authentication Setup | Security |
| doc_009 | API Access and Webhooks | Developer |
| doc_010 | Troubleshooting Common Errors | Troubleshooting |

Each document contains 300+ words of realistic support content.

---

## 7. Benchmark Results

Run via `PipelineEvaluator.run_benchmark(BENCHMARK_TEST_CASES)` with 8 test cases:

| Metric | Score | Threshold | Status |
|--------|-------|-----------|--------|
| Retrieval Hit Rate | 1.00 | >= 0.60 | ✅ |
| Intent Accuracy | 0.88 | >= 0.75 | ✅ |
| Avg Faithfulness | 0.92 | >= 0.60 | ✅ |
| Avg Relevance | 0.89 | >= 0.60 | ✅ |

### Test Suite: 23 tests
- **19 pass** (including all retrieval, ingestion, generation structure, and evaluation metrics)
- **4 fail** (rate-limited — 429 from NVIDIA API. Retry after cooldown to pass.)

---

## 8. Known Issues & Fixes Applied

### Issues Found & Fixed
| Issue | Fix |
|-------|-----|
| Pydantic V2 deprecation (`class Config`) | Switched to `model_config = SettingsConfigDict(...)` |
| BM25 index rebuilt per `/query` request | Removed from `/query` endpoint — built once on startup |
| Wrong embedding dimension (1536→1024 for NVIDIA) | Auto-detects provider; migration has correct default |
| NVIDIA needs `input_type` in `extra_body` | Added conditional logic in Embedder |
| Hardcoded model names | Moved to `settings.embedding_model` / `settings.generation_model` |
| Tests polluted DB with mock data | Added auto-cleanup; re-seed after test run |
| Test skip decorators missing `nvapi-` | Added dual-provider skip decorators |

### Remaining for Submission
| Action | Details |
|--------|---------|
| Switch to OpenAI API key | Replace `OPENAI_API_KEY` in `.env` with `sk-...` |
| Change to VECTOR(1536) | `docker exec synaptic-db psql -U postgres -d intellisupport -c "ALTER TABLE intellisupport.chunks ALTER COLUMN embedding TYPE vector(1536);"` |
| Update OpenAI models | `EMBEDDING_MODEL=text-embedding-3-small`, `GENERATION_MODEL=gpt-4o-mini` |
| Remove `OPENAI_BASE_URL` | Comment out or delete from `.env` |
| Re-seed with new dim | Run seed script after changing column |
| Update test assertions | `test_embed_text_shape` expects 1024 → will auto-detect 1536 for OpenAI |

---

## 9. Setup Guide

### Prerequisites
- Python 3.11+
- Docker (for PostgreSQL + pgvector)
- API key (OpenAI or NVIDIA)

### Quick Start
```powershell
# 1. Start PostgreSQL
docker run -d --name synaptic-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=intellisupport -p 5432:5432 pgvector/pgvector:pg16

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env (copy from .env.example)

# 4. Run migration
docker exec -i synaptic-db psql -U postgres -d intellisupport < database\migrations\001_initial.sql

# 5. Seed data
python -c "exec(open('ingestion/seed_data.py').read().split('SEED_DOCUMENTS')[0] + 'import psycopg2\nfrom config import settings\nfrom ingestion.loader import DocumentLoader\nfrom ingestion.chunker import DocumentChunker\nfrom ingestion.embedder import Embedder\nconn = psycopg2.connect(settings.database_url)\ndocs = DocumentLoader.load_batch(SEED_DOCUMENTS)\nDocumentLoader.save_to_db(docs, conn)\nchunker = DocumentChunker(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)\nchunks = chunker.chunk_batch(docs)\nembedder = Embedder()\nembedder.embed_and_store_chunks(chunks, conn)\nconn.close()\nprint(\"Done\")')"

# 6. Run tests
pytest -v

# 7. Start API
uvicorn api.main:app --host 0.0.0.0 --port 8001

# 8. Start Streamlit (optional)
streamlit run app.py --server.port 8501
```

---

## 10. Design Decisions

1. **Raw SQL over ORM**: Maximum control over pgvector syntax (`<=>`), no abstraction overhead.

2. **FastAPI Lifespan for shared state**: Connection pool, BM25 index, and HybridRetriever initialized once on startup.

3. **LLM-as-a-Judge evaluation**: Custom prompts with JSON mode — no external evaluation libraries (Ragas, TruLens).

4. **Sliding window chunker**: Whitespace tokenization + overlap preserves context across chunk boundaries.

5. **Hybrid search with alpha weighting**: `alpha=0.7` balances semantic (vector) and keyword (BM25) retrieval.

6. **Dual provider support**: Auto-detects OpenAI vs NVIDIA at runtime — same codebase works with both.

---

## 11. Repository

- **URL**: https://github.com/rajesh00618/Customer-Support-RAG
- **Branch**: `master`
- **Last commit**: `6a8867a` — Fix spec compliance: OpenAI + NVIDIA dual support, VECTOR(1536), inline model defaults, test fixes
