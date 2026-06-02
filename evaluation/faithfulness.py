import json
import logging
from typing import List
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from config import settings
from retrieval.vector_store import RetrievedChunk

logger = logging.getLogger(__name__)

class FaithfulnessResult(BaseModel):
    faithfulness_score: float
    total_claims: int
    supported_claims: int
    unsupported_claims: int
    reasoning: str

    @field_validator("faithfulness_score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("faithfulness_score must be between 0.0 and 1.0")
        return v

class FaithfulnessEvaluator:
    def __init__(self, model: str = None):
        self.model = model or settings.generation_model
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def evaluate(self, response_text: str, retrieved_chunks: List[RetrievedChunk]) -> FaithfulnessResult:
        """
        Constructs a prompt that presents:
        - The retrieved context (all chunks concatenated)
        - The generated response
        Asks the LLM-as-judge to identify claims in the response and classify each as supported or unsupported by the context
        The LLM must return a JSON response in this exact format:
        {
          "total_claims": 5,
          "supported_claims": 4,
          "unsupported_claims": 1,
          "reasoning": "..."
        }
        Computes faithfulness_score = supported_claims / total_claims
        If total_claims == 0, returns score of 1.0
        """
        if not response_text or not response_text.strip():
            return FaithfulnessResult(
                faithfulness_score=1.0,
                total_claims=0,
                supported_claims=0,
                unsupported_claims=0,
                reasoning="Response text is empty."
            )

        # Concatenate context chunks
        context_parts = []
        for idx, chunk in enumerate(retrieved_chunks):
            context_parts.append(f"Chunk {idx+1} (ID: {chunk.chunk_id}):\n{chunk.content}")
        context_str = "\n\n".join(context_parts) if context_parts else "No context chunks retrieved."

        system_prompt = """You are an expert AI evaluator assessing the faithfulness (grounding) of an AI assistant's response against the provided context chunks.
Your task is to:
1. Identify all individual factual claims made in the generated response.
2. For each claim, evaluate whether it is "supported" or "unsupported" by the context.
   - A claim is "supported" only if it can be directly verified from the provided context chunks.
   - If the context chunks do not address the claim, do not mention it, or if it is silent on it, it must be marked as "unsupported".
   - If the response states "I don't have information about that" or equivalent because the context was empty or insufficient, that is a faithful response, and the number of claims should be 0.
3. Count the total_claims, supported_claims, and unsupported_claims.
4. Output your evaluation in JSON format with exactly the keys: "total_claims", "supported_claims", "unsupported_claims", and "reasoning".

Reasoning should detail the claims extracted and the verification process for each.

Return JSON in this format:
{
  "total_claims": 5,
  "supported_claims": 4,
  "unsupported_claims": 1,
  "reasoning": "Claim 1: ... (Supported) | Claim 2: ... (Unsupported)"
}
"""

        user_content = (
            f"Retrieved Context:\n{context_str}\n\n"
            f"Generated Response:\n{response_text}"
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
            
            total_claims = int(data.get("total_claims", 0))
            supported_claims = int(data.get("supported_claims", 0))
            unsupported_claims = int(data.get("unsupported_claims", 0))
            reasoning = data.get("reasoning", "")
            
            # Recalculate or sanitize counts to avoid division errors or inconsistent counts
            if total_claims < 0:
                total_claims = 0
            if supported_claims < 0:
                supported_claims = 0
            if unsupported_claims < 0:
                unsupported_claims = 0
                
            # If totals don't sum, trust the breakdown
            if total_claims != (supported_claims + unsupported_claims):
                total_claims = supported_claims + unsupported_claims

            # Compute faithfulness score
            if total_claims == 0:
                faithfulness_score = 1.0
            else:
                faithfulness_score = supported_claims / total_claims
                
            return FaithfulnessResult(
                faithfulness_score=max(0.0, min(1.0, faithfulness_score)),
                total_claims=total_claims,
                supported_claims=supported_claims,
                unsupported_claims=unsupported_claims,
                reasoning=reasoning
            )
            
        except Exception as e:
            logger.error(f"Faithfulness evaluation failed: {e}")
            # Safe default fallback on error
            return FaithfulnessResult(
                faithfulness_score=0.0,
                total_claims=0,
                supported_claims=0,
                unsupported_claims=0,
                reasoning=f"Error running evaluator: {e}"
            )
