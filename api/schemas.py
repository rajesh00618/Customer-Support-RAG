from typing import List, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1)

class QueryResponse(BaseModel):
    query_id: str
    response_id: str
    response_text: str
    intent: str
    intent_confidence: float
    retrieved_chunk_ids: List[str]
    faithfulness_score: Optional[float] = None
    relevance_score: Optional[float] = None

class EvaluateResponse(BaseModel):
    response_id: str
    faithfulness_score: float
    relevance_score: float
    combined_score: float

class FeedbackRequest(BaseModel):
    response_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    feedback_id: str
    message: str = "Feedback recorded"

class HealthResponse(BaseModel):
    status: str = "ok"
    db_connected: bool
    chunks_indexed: int
