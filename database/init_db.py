import logging
import psycopg2
from config import settings

logger = logging.getLogger(__name__)

MIGRATION_SQL = """
CREATE SCHEMA IF NOT EXISTS intellisupport;
CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;

CREATE TABLE IF NOT EXISTS intellisupport.documents (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(64) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    source_url TEXT,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS intellisupport.chunks (
    id SERIAL PRIMARY KEY,
    chunk_id VARCHAR(64) UNIQUE NOT NULL,
    doc_id VARCHAR(64) REFERENCES intellisupport.documents(doc_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    token_count INTEGER,
    embedding VECTOR,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS intellisupport.queries (
    id SERIAL PRIMARY KEY,
    query_id VARCHAR(64) UNIQUE NOT NULL,
    raw_query TEXT NOT NULL,
    intent VARCHAR(64),
    intent_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS intellisupport.responses (
    id SERIAL PRIMARY KEY,
    response_id VARCHAR(64) UNIQUE NOT NULL,
    query_id VARCHAR(64) REFERENCES intellisupport.queries(query_id) ON DELETE CASCADE,
    response_text TEXT NOT NULL,
    retrieved_chunk_ids TEXT[],
    faithfulness_score FLOAT,
    relevance_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS intellisupport.feedback (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(64) UNIQUE NOT NULL,
    response_id VARCHAR(64) REFERENCES intellisupport.responses(response_id) ON DELETE CASCADE,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
"""


def init_database():
    """Run migrations and seed data if the chunks table is empty."""
    try:
        conn = psycopg2.connect(settings.database_url)
        conn.autocommit = True
        cur = conn.cursor()

        logger.info("Running database migrations...")
        cur.execute(MIGRATION_SQL)
        logger.info("Migrations complete.")

        cur.execute("SELECT COUNT(*) FROM intellisupport.chunks;")
        chunk_count = cur.fetchone()[0]

        if chunk_count == 0:
            logger.info("No chunks found — seeding documents and embeddings...")
            from ingestion.seed_data import SEED_DOCUMENTS
            from ingestion.loader import DocumentLoader
            from ingestion.chunker import DocumentChunker
            from ingestion.embedder import Embedder

            conn_seeded = psycopg2.connect(settings.database_url)
            docs = DocumentLoader.load_batch(SEED_DOCUMENTS)
            DocumentLoader.save_to_db(docs, conn_seeded)

            chunker = DocumentChunker(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )
            chunks = chunker.chunk_batch(docs)

            embedder = Embedder()
            embedder.embed_and_store_chunks(chunks, conn_seeded)
            conn_seeded.close()

            logger.info(f"Seeded {len(docs)} documents and {len(chunks)} chunks.")
        else:
            logger.info(f"Database already has {chunk_count} chunks — skipping seed.")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False
