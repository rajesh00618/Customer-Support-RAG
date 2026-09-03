import logging
from typing import List
from pydantic import BaseModel
from retrieval.vector_store import RetrievedChunk
from evaluation.faithfulness import FaithfulnessEvaluator, FaithfulnessResult
from evaluation.relevance import RelevanceEvaluator, RelevanceResult
from classification.intent_classifier import IntentClassifier
from ingestion.embedder import Embedder
from retrieval.vector_store import VectorStore
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever
from generation.prompt_builder import PromptBuilder
from generation.response_generator import ResponseGenerator
from config import settings

logger = logging.getLogger(__name__)

class EvaluationReport(BaseModel):
    query_id: str
    response_id: str
    faithfulness_score: float
    relevance_score: float
    combined_score: float     # average of faithfulness and relevance

class BenchmarkReport(BaseModel):
    total_cases: int
    avg_faithfulness: float
    avg_relevance: float
    avg_combined: float
    retrieval_hit_rate: float    # fraction of cases where expected doc was retrieved
    intent_accuracy: float       # fraction of cases with correct intent classification

class PipelineEvaluator:
    def __init__(self, faithfulness_evaluator: FaithfulnessEvaluator, relevance_evaluator: RelevanceEvaluator, conn):
        self.faithfulness_evaluator = faithfulness_evaluator
        self.relevance_evaluator = relevance_evaluator
        self.conn = conn

    def evaluate_response(self, query_id: str, response_id: str) -> EvaluationReport:
        """
        Loads the query, response, and retrieved chunks from the database using query_id and response_id
        Runs both FaithfulnessEvaluator.evaluate and RelevanceEvaluator.evaluate
        Updates intellisupport.responses with computed faithfulness_score and relevance_score
        Returns an EvaluationReport
        """
        raw_query = ""
        response_text = ""
        retrieved_chunk_ids = []

        with self.conn.cursor() as cur:
            # 1. Get raw query
            cur.execute(
                "SELECT raw_query FROM intellisupport.queries WHERE query_id = %s;",
                (query_id,)
            )
            q_row = cur.fetchone()
            if not q_row:
                raise ValueError(f"Query with ID '{query_id}' not found in database.")
            raw_query = q_row[0]

            # 2. Get response details
            cur.execute(
                "SELECT response_text, retrieved_chunk_ids FROM intellisupport.responses WHERE response_id = %s;",
                (response_id,)
            )
            r_row = cur.fetchone()
            if not r_row:
                raise ValueError(f"Response with ID '{response_id}' not found in database.")
            response_text, retrieved_chunk_ids = r_row

        # 3. Load retrieved chunks content
        retrieved_chunks = []
        if retrieved_chunk_ids:
            with self.conn.cursor() as cur:
                # Use ANY(%s) to query text array
                cur.execute(
                    "SELECT chunk_id, doc_id, content FROM intellisupport.chunks WHERE chunk_id = ANY(%s);",
                    (retrieved_chunk_ids,)
                )
                c_rows = cur.fetchall()
                # Create RetrievedChunk models
                for row in c_rows:
                    cid, did, content = row
                    retrieved_chunks.append(
                        RetrievedChunk(
                            chunk_id=cid,
                            doc_id=did,
                            content=content,
                            score=1.0,  # Placeholder score since it is not saved in DB
                            retrieval_method="hybrid"  # Placeholder method
                        )
                    )

        # 4. Evaluate
        faith_result = self.faithfulness_evaluator.evaluate(response_text, retrieved_chunks)
        relevance_result = self.relevance_evaluator.evaluate(raw_query, retrieved_chunks)

        # 5. Save scores to database
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE intellisupport.responses
                SET faithfulness_score = %s, relevance_score = %s
                WHERE response_id = %s;
                """,
                (faith_result.faithfulness_score, relevance_result.relevance_score, response_id)
            )
            self.conn.commit()

        combined_score = (faith_result.faithfulness_score + relevance_result.relevance_score) / 2.0

        return EvaluationReport(
            query_id=query_id,
            response_id=response_id,
            faithfulness_score=faith_result.faithfulness_score,
            relevance_score=relevance_result.relevance_score,
            combined_score=combined_score
        )

    def run_benchmark(self, test_cases: List[dict]) -> BenchmarkReport:
        """
        Accepts a list of test case dicts with keys: query, expected_doc_ids, expected_intent
        For each test case:
        - Classifies the query intent
        - Embeds the query
        - Retrieves chunks using HybridRetriever
        - Checks if any retrieved chunk's doc_id appears in expected_doc_ids — this is retrieval_hit (True/False)
        - Generates a response
        - Evaluates faithfulness and relevance
        Returns a BenchmarkReport with aggregate metrics
        """
        if not test_cases:
            return BenchmarkReport(
                total_cases=0,
                avg_faithfulness=0.0,
                avg_relevance=0.0,
                avg_combined=0.0,
                retrieval_hit_rate=0.0,
                intent_accuracy=0.0
            )

        # Instantiate components needed for the benchmark run
        intent_classifier = IntentClassifier()
        embedder = Embedder()
        vector_store = VectorStore(self.conn)
        bm25_retriever = BM25Retriever(self.conn)
        hybrid_retriever = HybridRetriever(vector_store, bm25_retriever, alpha=settings.hybrid_alpha)
        response_generator = ResponseGenerator()

        total_cases = len(test_cases)
        correct_intents = 0
        retrieval_hits = 0
        sum_faithfulness = 0.0
        sum_relevance = 0.0

        for case in test_cases:
            query = case["query"]
            expected_doc_ids = case["expected_doc_ids"]
            expected_intent = case["expected_intent"]

            # 1. Classify intent
            intent_res = intent_classifier.classify(query)
            if intent_res.intent == expected_intent:
                correct_intents += 1

            # 2. Embed query
            query_embedding = embedder.embed_text(query)

            # 3. Retrieve chunks (with Jaccard reranking, matching the README architecture)
            retrieved_chunks = hybrid_retriever.retrieve_with_reranking(query, query_embedding, top_k=settings.top_k)

            # 4. Check retrieval hit
            retrieved_doc_ids = {c.doc_id for c in retrieved_chunks}
            hit = any(doc_id in retrieved_doc_ids for doc_id in expected_doc_ids)
            if hit:
                retrieval_hits += 1

            # 5. Build prompts
            if not retrieved_chunks:
                messages = PromptBuilder.build_clarification_prompt(query, intent_res)
            else:
                messages = PromptBuilder.build_rag_prompt(query, retrieved_chunks, intent_res)
                
            fallback_messages = PromptBuilder.build_clarification_prompt(query, intent_res)

            # 6. Generate Response
            gen_response = response_generator.generate_with_fallback(messages, fallback_messages)

            # 7. Run Evaluators
            faith_res = self.faithfulness_evaluator.evaluate(gen_response.response_text, retrieved_chunks)
            relevance_res = self.relevance_evaluator.evaluate(query, retrieved_chunks)

            sum_faithfulness += faith_res.faithfulness_score
            sum_relevance += relevance_res.relevance_score

        # Compute averages
        avg_faithfulness = sum_faithfulness / total_cases
        avg_relevance = sum_relevance / total_cases
        avg_combined = (avg_faithfulness + avg_relevance) / 2.0
        retrieval_hit_rate = retrieval_hits / total_cases
        intent_accuracy = correct_intents / total_cases

        return BenchmarkReport(
            total_cases=total_cases,
            avg_faithfulness=avg_faithfulness,
            avg_relevance=avg_relevance,
            avg_combined=avg_combined,
            retrieval_hit_rate=retrieval_hit_rate,
            intent_accuracy=intent_accuracy
        )
