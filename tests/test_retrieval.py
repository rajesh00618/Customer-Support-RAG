import pytest
import psycopg2
from config import settings
from retrieval.vector_store import VectorStore, RetrievedChunk
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever

# Helper fixture for DB connection
@pytest.fixture(scope="module")
def conn():
    connection = psycopg2.connect(settings.database_url)
    yield connection
    connection.rollback()
    connection.close()

# Seed mock database with 5 distinct chunks
@pytest.fixture(scope="module", autouse=True)
def seed_data(conn):
    with conn.cursor() as cur:
        # Clear tables
        cur.execute("TRUNCATE intellisupport.feedback, intellisupport.responses, intellisupport.queries, intellisupport.chunks, intellisupport.documents CASCADE;")
        
        # Insert documents
        cur.execute(
            """
            INSERT INTO intellisupport.documents (doc_id, title, content)
            VALUES 
            ('doc_003', 'Billing and Subscription Plans', 'We offer three billing and subscription plans: Basic, Pro, and Enterprise.'),
            ('doc_008', 'Two-Factor Authentication Setup', 'To enable two-factor authentication 2FA, go to Settings, Account, Security and check 2FA.');
            """
        )
        
        # Insert chunks with mock embeddings
        # Chunk 1
        emb_003 = [0.1] * 1024
        emb_003_str = "[" + ",".join(map(str, emb_003)) + "]"
        cur.execute(
            """
            INSERT INTO intellisupport.chunks (chunk_id, doc_id, content, chunk_index, token_count, embedding)
            VALUES ('chunk_doc_003_0', 'doc_003', 'We offer three billing and subscription plans: Basic, Pro, and Enterprise.', 0, 10, %s::vector);
            """,
            (emb_003_str,)
        )
        
        # Chunk 2
        emb_008 = [0.9] * 1024
        emb_008_str = "[" + ",".join(map(str, emb_008)) + "]"
        cur.execute(
            """
            INSERT INTO intellisupport.chunks (chunk_id, doc_id, content, chunk_index, token_count, embedding)
            VALUES ('chunk_doc_008_0', 'doc_008', 'To enable two-factor authentication 2FA, go to Settings, Account, Security and check 2FA.', 0, 14, %s::vector);
            """,
            (emb_008_str,)
        )
        
        # Chunks 3, 4, 5 (for vector search size requirements)
        for i in range(3):
            emb_other = [0.5 + 0.05 * i] * 1024
            emb_other_str = "[" + ",".join(map(str, emb_other)) + "]"
            cur.execute(
                f"""
                INSERT INTO intellisupport.chunks (chunk_id, doc_id, content, chunk_index, token_count, embedding)
                VALUES ('chunk_doc_other_{i}', 'doc_003', 'Extra helper chunk text {i} for testing.', {i+1}, 8, %s::vector);
                """,
                (emb_other_str,)
            )
            
        conn.commit()

def test_vector_similarity_search_returns_k_results(conn):
    vector_store = VectorStore(conn)
    query_emb = [0.1] * 1024
    results = vector_store.similarity_search(query_emb, top_k=5)
    assert len(results) == 5

def test_vector_similarity_scores_range(conn):
    vector_store = VectorStore(conn)
    query_emb = [0.1] * 1024
    results = vector_store.similarity_search(query_emb, top_k=5)
    for res in results:
        assert 0.0 <= res.score <= 1.0

def test_bm25_search_returns_results(conn):
    retriever = BM25Retriever(conn)
    results = retriever.search("billing subscription", top_k=5)
    assert len(results) >= 1
    # Check if doc_003 is matched
    match = any(res.doc_id == "doc_003" for res in results)
    assert match

def test_bm25_keyword_relevance(conn):
    retriever = BM25Retriever(conn)
    results = retriever.search("two factor authentication", top_k=5)
    # Check that doc_008 appears in the top-3 results
    top_3_doc_ids = [res.doc_id for res in results[:3]]
    assert "doc_008" in top_3_doc_ids

def test_hybrid_retriever_score_range(conn):
    vector_store = VectorStore(conn)
    bm25_retriever = BM25Retriever(conn)
    hybrid_retriever = HybridRetriever(vector_store, bm25_retriever, alpha=0.7)
    
    query_emb = [0.5] * 1024
    results = hybrid_retriever.retrieve("two factor authentication", query_emb, top_k=5)
    
    for res in results:
        assert 0.0 <= res.score <= 1.0

def test_hybrid_deduplication(conn):
    vector_store = VectorStore(conn)
    bm25_retriever = BM25Retriever(conn)
    hybrid_retriever = HybridRetriever(vector_store, bm25_retriever, alpha=0.7)
    
    query_emb = [0.9] * 1024
    results = hybrid_retriever.retrieve("two factor authentication 2FA", query_emb, top_k=5)
    
    # Assert no duplicate chunk ids
    chunk_ids = [res.chunk_id for res in results]
    assert len(chunk_ids) == len(set(chunk_ids))
