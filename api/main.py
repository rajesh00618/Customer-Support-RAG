import logging
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.pool import ThreadedConnectionPool

from config import settings
from api.schemas import (
    QueryRequest,
    QueryResponse,
    EvaluateResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
)
from ingestion.embedder import Embedder
from retrieval.vector_store import VectorStore
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever
from classification.intent_classifier import IntentClassifier
from generation.prompt_builder import PromptBuilder
from generation.response_generator import ResponseGenerator
from evaluation.faithfulness import FaithfulnessEvaluator
from evaluation.relevance import RelevanceEvaluator
from evaluation.evaluator import PipelineEvaluator
from feedback.feedback_store import FeedbackStore, FeedbackSummary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from database.init_db import init_database

    logger.info("Initializing database (migrations + seed if needed)...")
    init_database()

    logger.info("Initializing database connection pool...")
    pool = ThreadedConnectionPool(1, 20, dsn=settings.database_url)
    app.state.db_pool = pool

    conn = pool.getconn()
    try:
        logger.info("Initializing vector store and retrievers...")
        vector_store = VectorStore(conn)
        bm25_retriever = BM25Retriever(conn)
        hybrid_retriever = HybridRetriever(
            vector_store, bm25_retriever, alpha=settings.hybrid_alpha
        )

        app.state.vector_store = vector_store
        app.state.bm25_retriever = bm25_retriever
        app.state.hybrid_retriever = hybrid_retriever

        # Per-request LLM components are created once and shared across requests
        # (clients are stateless; only the model name is fixed at startup)
        app.state.intent_classifier = IntentClassifier()
        app.state.embedder = Embedder()
        app.state.response_generator = ResponseGenerator()
        app.state.faithfulness_evaluator = FaithfulnessEvaluator()
        app.state.relevance_evaluator = RelevanceEvaluator()
    finally:
        pool.putconn(conn)

    yield

    logger.info("Closing database connection pool...")
    app.state.db_pool.closeall()


app = FastAPI(
    title="IntelliSupport Autonomous Customer Support Platform",
    description="Production-grade autonomous AI customer support platform powered by FastAPI, pgvector, and OpenAI.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db(request: Request):
    pool = request.app.state.db_pool
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)


@app.post("/query", response_model=QueryResponse)
def post_query(request_body: QueryRequest, request: Request, conn=Depends(get_db)):
    query_text = request_body.query
    top_k = request_body.top_k
    hybrid_retriever = request.app.state.hybrid_retriever

    try:
        intent_classifier = request.app.state.intent_classifier
        intent_res = intent_classifier.classify(query_text)
        query_id = f"qry_{uuid4().hex[:8]}"

        embedder = request.app.state.embedder
        query_embedding = embedder.embed_text(query_text)

        # Jaccard reranker (README architecture): hybrid candidates re-ranked
        # by token-overlap with the query before prompt construction
        retrieved_chunks = hybrid_retriever.retrieve_with_reranking(
            query_text, query_embedding, top_k=top_k
        )
        chunk_ids = [c.chunk_id for c in retrieved_chunks]

        if not retrieved_chunks:
            messages = PromptBuilder.build_clarification_prompt(query_text, intent_res)
        else:
            messages = PromptBuilder.build_rag_prompt(
                query_text, retrieved_chunks, intent_res
            )

        fallback_messages = PromptBuilder.build_clarification_prompt(
            query_text, intent_res
        )

        response_generator = request.app.state.response_generator
        gen_response = response_generator.generate_with_fallback(
            messages, fallback_messages
        )
        response_id = f"rsp_{uuid4().hex[:8]}"

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO intellisupport.queries (query_id, raw_query, intent, intent_confidence, created_at)
                VALUES (%s, %s, %s, %s, NOW());
                """,
                (query_id, query_text, intent_res.intent, intent_res.confidence),
            )
            cur.execute(
                """
                INSERT INTO intellisupport.responses (response_id, query_id, response_text, retrieved_chunk_ids, created_at)
                VALUES (%s, %s, %s, %s, NOW());
                """,
                (response_id, query_id, gen_response.response_text, chunk_ids),
            )
            conn.commit()

        return QueryResponse(
            query_id=query_id,
            response_id=response_id,
            response_text=gen_response.response_text,
            intent=intent_res.intent,
            intent_confidence=intent_res.confidence,
            retrieved_chunk_ids=chunk_ids,
            faithfulness_score=None,
            relevance_score=None,
        )

    except Exception as e:
        logger.error(f"Error handling query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate/{response_id}", response_model=EvaluateResponse)
def post_evaluate(response_id: str, request: Request, conn=Depends(get_db)):
    faith_eval = request.app.state.faithfulness_evaluator
    relevance_eval = request.app.state.relevance_evaluator

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT query_id FROM intellisupport.responses WHERE response_id = %s;",
                (response_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(
                    status_code=404, detail=f"Response '{response_id}' not found."
                )
            query_id = row[0]

        evaluator = PipelineEvaluator(faith_eval, relevance_eval, conn)
        report = evaluator.evaluate_response(query_id, response_id)

        return EvaluateResponse(
            response_id=response_id,
            faithfulness_score=report.faithfulness_score,
            relevance_score=report.relevance_score,
            combined_score=report.combined_score,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error during response evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback", response_model=FeedbackResponse)
def post_feedback(feedback_body: FeedbackRequest, conn=Depends(get_db)):
    store = FeedbackStore(conn)
    try:
        fb_id = store.store_feedback(
            response_id=feedback_body.response_id,
            rating=feedback_body.rating,
            comment=feedback_body.comment,
        )
        return FeedbackResponse(feedback_id=fb_id, message="Feedback recorded")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/feedback/summary/{response_id}", response_model=FeedbackSummary)
def get_feedback_summary(response_id: str, conn=Depends(get_db)):
    store = FeedbackStore(conn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM intellisupport.responses WHERE response_id = %s;",
                (response_id,),
            )
            if not cur.fetchone():
                raise HTTPException(
                    status_code=404, detail=f"Response '{response_id}' not found."
                )

        return store.get_feedback_summary(response_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching feedback summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
def get_health(conn=Depends(get_db)):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM intellisupport.chunks;")
            chunks_count = cur.fetchone()[0]

        return HealthResponse(
            status="ok", db_connected=True, chunks_indexed=chunks_count
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(status="error", db_connected=False, chunks_indexed=0)
