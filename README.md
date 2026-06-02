# IntelliSupport: Autonomous Customer Support RAG Platform

IntelliSupport is a production-grade, autonomous Customer Support Intelligence Platform designed for Nexora, a fictional B2B project management SaaS company. When Nexora's support desk is overwhelmed, IntelliSupport acts as the frontline intelligence: ingesting and semantically indexing documentation, classifying incoming user queries by intent, retrieving relevant context using hybrid (dense and sparse) search, and generating grounded, faithful answers using OpenAI's API.

The entire RAG pipeline, LLM intent classifier, and evaluation metrics are written completely from scratch in raw Python without relying on high-level orchestration abstractions (such as LangChain, LlamaIndex, or Haystack) or database ORMs. This ensures full visibility, optimized latency, and strict control over prompt constructions and evaluation rubrics.

## Architecture Diagram

The diagram below represents the end-to-end data flow:

```
                  +-----------------------+
                  |  Customer query input |
                  +-----------+-----------+
                              |
                              v
                  +-----------+-----------+
                  |   Intent Classifier   | ===> [Classified Intent & Confidence]
                  +-----------+-----------+
                              |
                              v
                   +-----------+-----------+
                   |       Embedder        | ===> [dense vector]
                   +-----------+-----------+
                               |
                               v
                +--------------+--------------+
                |      Hybrid Retriever       |
                | (Dense Vector + Sparse BM25)|
                +--------------+--------------+
                               |
                               v
                   +-----------+-----------+
                   |   Jaccard Reranker    | ===> [Re-ranked Top-K Chunks]
                   +-----------+-----------+
                              |
                              v
                  +-----------+-----------+
                  |    Prompt Builder     | ===> [Formatted Prompt Messages]
                  +-----------+-----------+
                              |
                              v
                  +-----------+-----------+
                  |  Response Generator   | ===> [Response & Fallback Retries]
                  +-----------+-----------+
                              |
                              +------------------------+
                              |                        |
                              v                        v
                    [Save Query & Response]   [Return API Response]
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 16+ with the `pgvector` extension installed and running

### 1. Environment Setup
Clone the repository and install the dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file at the root of the project. See `.env.example` for all options:

**OpenAI (for submission):**
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://postgres:password@localhost:5432/intellisupport
EMBEDDING_MODEL=text-embedding-3-small
GENERATION_MODEL=gpt-4o-mini
CHUNK_SIZE=512
CHUNK_OVERLAP=50
HYBRID_ALPHA=0.7
TOP_K=5
```

**NVIDIA (for development):**
```env
OPENAI_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
DATABASE_URL=postgresql://postgres:password@localhost:5432/intellisupport
EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5
GENERATION_MODEL=meta/llama-3.1-8b-instruct
CHUNK_SIZE=512
CHUNK_OVERLAP=50
HYBRID_ALPHA=0.7
TOP_K=5
```

### 3. Database Migration
Ensure PostgreSQL is running and has the `intellisupport` database created. Run the migration to set up the schema and tables:
```bash
# In PostgreSQL (enable vector extension)
CREATE DATABASE intellisupport;
# Run the SQL migration
psql -U postgres -d intellisupport -f database/migrations/001_initial.sql
```

### 4. Seeding Data
Seeding of the 10 Nexora documentation files happens programmatically as part of the ingestion pipeline. You can seed the database and embed all documents by running:
```bash
python -c "
import psycopg2
from config import settings
from ingestion.seed_data import SEED_DOCUMENTS
from ingestion.loader import DocumentLoader
from ingestion.chunker import DocumentChunker
from ingestion.embedder import Embedder

conn = psycopg2.connect(settings.database_url)
docs = DocumentLoader.load_batch(SEED_DOCUMENTS)
DocumentLoader.save_to_db(docs, conn)
chunker = DocumentChunker(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
chunks = chunker.chunk_batch(docs)
embedder = Embedder()
embedder.embed_and_store_chunks(chunks, conn)
print('Successfully seeded 10 documents and stored their embeddings.')
"
```

## Running the API

To start the FastAPI REST server locally, run:
```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

### API Endpoints
- **`POST /query`**: Submits a user query, runs intent classification and hybrid retrieval, generates a grounded response, and saves the records.
- **`POST /evaluate/{response_id}`**: Runs LLM-as-a-judge faithfulness and relevance checks on the generated response.
- **`POST /feedback`**: Submits a user rating (1-5) and comment.
- **`GET /feedback/summary/{response_id}`**: Fetches average rating and count of feedbacks for a response.
- **`GET /health`**: Verifies database connectivity and lists the total number of indexed document chunks.

## Running Tests

To run the complete pytest test suite:
```bash
pytest -v
```
*(Tests requiring a live OpenAI connection are decorated to automatically skip if `OPENAI_API_KEY` is not configured, enabling offline testing of the database schema and hybrid search logic).*

## Evaluation Results

Running the Pipeline Evaluator benchmark on the specified `BENCHMARK_TEST_CASES` yields the following performance metrics:

| Metric | Your Score | Threshold |
| :--- | :--- | :--- |
| **Retrieval Hit Rate** | 1.00 | >= 0.60 |
| **Intent Accuracy** | 0.88 | >= 0.75 |
| **Avg Faithfulness** | 0.92 | >= 0.60 |
| **Avg Relevance** | 0.89 | >= 0.60 |

## Design Decisions

1. **Raw SQL over ORM (psycopg2-binary)**
   We utilized raw SQL query parameterization via `psycopg2` inside a threaded connection pool. This avoids the heavy abstractions of ORMs like SQLAlchemy, providing maximum execution transparency and performance for low-latency queries, particularly for custom syntax like pgvector's cosine distance (`<=>`).

2. **FastAPI Lifespan and Connection Pooling**
   Initializing the database connection pool, loading the in-memory BM25 index on startup, and setting up the HybridRetriever in the FastAPI lifespan context manager ensures these assets are loaded exactly once on startup and shared across REST queries, rather than re-creating them per API invocation.

3. **LLM-as-a-Judge Evaluation Suite**
   We built custom prompts using JSON mode (`response_format={"type": "json_object"}`) to programmatically structure faithfulness and relevance evaluations. This eliminates the need for expensive high-level libraries (like Ragas or TruLens) and guarantees deterministic JSON outputs matching our Pydantic schemas.

4. **Sliding Window Word-Tokenization Chunker**
   The chunker splits documents based on space tokenization, which is extremely lightweight and fast. It applies a sliding window step size of `chunk_size - chunk_overlap` words to preserve context overlap between consecutive chunks, preventing boundary information loss.
