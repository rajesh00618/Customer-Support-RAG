import pytest
import psycopg2
from config import settings
from evaluation.faithfulness import FaithfulnessEvaluator, FaithfulnessResult
from evaluation.relevance import RelevanceEvaluator, RelevanceResult
from evaluation.evaluator import PipelineEvaluator, EvaluationReport, BenchmarkReport
from retrieval.vector_store import RetrievedChunk

# High-priority benchmark test cases as specified in Phase 4.4
BENCHMARK_TEST_CASES = [
    {
        "query": "How do I add a new member to my team?",
        "expected_doc_ids": ["doc_002"],
        "expected_intent": "account_management"
    },
    {
        "query": "What happens if I cancel my subscription?",
        "expected_doc_ids": ["doc_003"],
        "expected_intent": "billing"
    },
    {
        "query": "How do I connect Nexora to Slack?",
        "expected_doc_ids": ["doc_004"],
        "expected_intent": "integration"
    },
    {
        "query": "I forgot my password and can't log in",
        "expected_doc_ids": ["doc_008", "doc_002"],
        "expected_intent": "account_management"
    },
    {
        "query": "How do I export my project data as CSV?",
        "expected_doc_ids": ["doc_007"],
        "expected_intent": "data_and_export"
    },
    {
        "query": "The webhook I set up isn't receiving any events",
        "expected_doc_ids": ["doc_009"],
        "expected_intent": "technical_issue"
    },
    {
        "query": "Can I use custom templates for new projects?",
        "expected_doc_ids": ["doc_005"],
        "expected_intent": "feature_request"
    },
    {
        "query": "How do I enable two-factor authentication for my account?",
        "expected_doc_ids": ["doc_008"],
        "expected_intent": "account_management"
    }
]

# Helper fixture for DB connection
@pytest.fixture(scope="module")
def conn():
    connection = psycopg2.connect(settings.database_url)
    yield connection
    connection.rollback()
    connection.close()

# Decorator to skip tests if no API key is provided
openai_test = pytest.mark.skipif(
    settings.openai_api_key in ("your-openai-api-key-here", "your-nvidia-api-key-here")
    or not (settings.openai_api_key.startswith("sk-") or settings.openai_api_key.startswith("nvapi-")),
    reason="Requires a valid OpenAI/NVIDIA API key"
)

# Seeding fixture: seeds all 10 documents if API key is active
@pytest.fixture(scope="module", autouse=True)
def seed_all_docs(conn):
    if settings.openai_api_key in ("your-openai-api-key-here", "your-nvidia-api-key-here") \
       or not (settings.openai_api_key.startswith("sk-") or settings.openai_api_key.startswith("nvapi-")):
        return
        
    from ingestion.seed_data import SEED_DOCUMENTS
    from ingestion.loader import DocumentLoader
    from ingestion.chunker import DocumentChunker
    from ingestion.embedder import Embedder
    
    # 1. Clear database tables
    with conn.cursor() as cur:
        cur.execute("TRUNCATE intellisupport.feedback, intellisupport.responses, intellisupport.queries, intellisupport.chunks, intellisupport.documents CASCADE;")
        conn.commit()
        
    # 2. Load and save documents
    docs = DocumentLoader.load_batch(SEED_DOCUMENTS)
    DocumentLoader.save_to_db(docs, conn)
    
    # 3. Chunk documents
    chunker = DocumentChunker(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    chunks = chunker.chunk_batch(docs)
    
    # 4. Embed and store chunks
    embedder = Embedder()
    embedder.embed_and_store_chunks(chunks, conn)

@openai_test
def test_faithfulness_score_range():
    evaluator = FaithfulnessEvaluator()
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_doc_001_0",
            doc_id="doc_001",
            content="Nexora workspaces can be customized by adding users.",
            score=0.9,
            retrieval_method="hybrid"
        )
    ]
    response = "You can customize Nexora workspaces by adding users to them."
    res = evaluator.evaluate(response, chunks)
    assert isinstance(res, FaithfulnessResult)
    assert 0.0 <= res.faithfulness_score <= 1.0

@openai_test
def test_relevance_score_range():
    evaluator = RelevanceEvaluator()
    chunks = [
        RetrievedChunk(
            chunk_id="chunk_doc_001_0",
            doc_id="doc_001",
            content="Nexora workspaces can be customized by adding users.",
            score=0.9,
            retrieval_method="hybrid"
        )
    ]
    res = evaluator.evaluate("How do I customize my workspace?", chunks)
    assert isinstance(res, RelevanceResult)
    assert 0.0 <= res.relevance_score <= 1.0

@openai_test
def test_benchmark_hit_rate(conn):
    faith_eval = FaithfulnessEvaluator()
    rel_eval = RelevanceEvaluator()
    pipeline_eval = PipelineEvaluator(faith_eval, rel_eval, conn)
    
    report = pipeline_eval.run_benchmark(BENCHMARK_TEST_CASES)
    assert isinstance(report, BenchmarkReport)
    assert report.retrieval_hit_rate >= 0.6

@openai_test
def test_benchmark_intent_accuracy(conn):
    faith_eval = FaithfulnessEvaluator()
    rel_eval = RelevanceEvaluator()
    pipeline_eval = PipelineEvaluator(faith_eval, rel_eval, conn)
    
    report = pipeline_eval.run_benchmark(BENCHMARK_TEST_CASES)
    assert report.intent_accuracy >= 0.75

@openai_test
def test_benchmark_avg_faithfulness(conn):
    faith_eval = FaithfulnessEvaluator()
    rel_eval = RelevanceEvaluator()
    pipeline_eval = PipelineEvaluator(faith_eval, rel_eval, conn)
    
    report = pipeline_eval.run_benchmark(BENCHMARK_TEST_CASES)
    assert report.avg_faithfulness >= 0.6
