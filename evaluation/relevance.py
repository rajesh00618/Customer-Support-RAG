import json
import logging
from typing import List, Tuple
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from config import settings
from retrieval.vector_store import RetrievedChunk

logger = logging.getLogger(__name__)

class ChunkRelevanceScore(BaseModel):
    chunk_id: str
    score: int
    reason: str

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: int) -> int:
        if v not in (0, 1, 2):
            raise ValueError("Relevance score must be 0, 1, or 2")
        return v

class RelevanceResult(BaseModel):
    relevance_score: float
    chunk_scores: List[ChunkRelevanceScore]
    query: str

    @field_validator("relevance_score")
    @classmethod
    def validate_relevance_score(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("relevance_score must be between 0.0 and 1.0")
        return v

class RelevanceEvaluator:
    def __init__(self, model: str = None):
        self.model = model or settings.generation_model
        base_url = settings.openai_base_url or None
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=base_url)

    def evaluate(self, query: str, retrieved_chunks: List[RetrievedChunk]) -> RelevanceResult:
        """
        For each retrieved chunk, asks the LLM to rate its relevance to the query on a scale of 0–2:
        0 = Not relevant
        1 = Partially relevant
        2 = Highly relevant
        The LLM must return JSON:
        {
          "chunk_scores": [
            {"chunk_id": "chunk_doc_001_0", "score": 2, "reason": "..."},
            ...
          ]
        }
        Computes relevance_score = sum(chunk_scores) / (2 * len(chunks))
        Returns normalized score from 0.0 to 1.0
        """
        if not query or not query.strip():
            return RelevanceResult(relevance_score=0.0, chunk_scores=[], query="")
            
        if not retrieved_chunks:
            return RelevanceResult(relevance_score=0.0, chunk_scores=[], query=query)

        # Build chunks text to present to LLM
        chunks_str = ""
        for idx, chunk in enumerate(retrieved_chunks):
            chunks_str += f"Chunk ID: {chunk.chunk_id}\nContent: {chunk.content}\n---\n"

        system_prompt = """You are an expert AI evaluator assessing the relevance of retrieved documentation chunks to a customer's query.
For each chunk provided, assign a relevance score of 0, 1, or 2:
- 0: Not relevant. The chunk contains no useful information related to the query and cannot help answer it.
- 1: Partially relevant. The chunk mentions relevant keywords or topics but is missing crucial details to fully answer the query.
- 2: Highly relevant. The chunk directly addresses the query and contains the necessary details to answer it.

You must respond in JSON format with exactly the key: "chunk_scores", which is an array of objects. Each object must have:
- "chunk_id": the exact chunk_id string of the chunk.
- "score": the integer score (0, 1, or 2).
- "reason": a short explanation of why the score was given.

Return JSON in this format:
{
  "chunk_scores": [
    {"chunk_id": "chunk_doc_001_0", "score": 2, "reason": "Directly explains how to add team members."}
  ]
}
"""

        user_content = (
            f"Query: {query}\n\n"
            f"Retrieved Chunks:\n{chunks_str}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            result_text = response.choices[0].message.content
            data = json.loads(result_text)
            
            scores_data = data.get("chunk_scores", [])
            chunk_scores = []
            
            # Map chunk_scores
            scores_map = {}
            for item in scores_data:
                cid = item.get("chunk_id")
                score = item.get("score")
                reason = item.get("reason", "")
                
                try:
                    score_int = int(score)
                    if score_int not in (0, 1, 2):
                        score_int = 0
                except (ValueError, TypeError):
                    score_int = 0
                    
                if cid:
                    scores_map[cid] = ChunkRelevanceScore(chunk_id=cid, score=score_int, reason=reason)
                    
            # Ensure every retrieved chunk is accounted for, using 0 as fallback if LLM skipped it
            final_scores = []
            total_sum = 0
            for chunk in retrieved_chunks:
                score_obj = scores_map.get(chunk.chunk_id)
                if not score_obj:
                    score_obj = ChunkRelevanceScore(chunk_id=chunk.chunk_id, score=0, reason="Not evaluated by LLM.")
                final_scores.append(score_obj)
                total_sum += score_obj.score

            # Compute normalized score
            num_chunks = len(retrieved_chunks)
            relevance_score = total_sum / (2.0 * num_chunks)
            
            return RelevanceResult(
                relevance_score=max(0.0, min(1.0, relevance_score)),
                chunk_scores=final_scores,
                query=query
            )
            
        except Exception as e:
            logger.error(f"Relevance evaluation failed: {e}")
            # Fallback
            fallback_scores = [
                ChunkRelevanceScore(chunk_id=c.chunk_id, score=0, reason=f"Evaluator error: {e}")
                for c in retrieved_chunks
            ]
            return RelevanceResult(
                relevance_score=0.0,
                chunk_scores=fallback_scores,
                query=query
            )

    def evaluate_batch(self, queries_and_chunks: List[Tuple[str, List[RetrievedChunk]]]) -> List[RelevanceResult]:
        """
        Evaluates multiple query-chunk pairs
        Returns results in same order
        """
        return [self.evaluate(q, chunks) for q, chunks in queries_and_chunks]
