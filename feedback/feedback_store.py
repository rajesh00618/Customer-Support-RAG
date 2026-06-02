import logging
from uuid import uuid4
from pydantic import BaseModel
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FeedbackSummary(BaseModel):
    response_id: str
    avg_rating: float
    total_count: int

class FeedbackStore:
    def __init__(self, conn):
        self.conn = conn

    def store_feedback(self, response_id: str, rating: int, comment: str = None) -> str:
        """
        Validates rating is between 1 and 5; raises ValueError if not
        Generates feedback_id as f"fb_{uuid4().hex[:8]}"
        Inserts into intellisupport.feedback
        Returns feedback_id
        """
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5 inclusive.")
            
        feedback_id = f"fb_{uuid4().hex[:8]}"
        
        with self.conn.cursor() as cur:
            # Check if response exists first (to respect database integrity constraint)
            cur.execute("SELECT 1 FROM intellisupport.responses WHERE response_id = %s;", (response_id,))
            if not cur.fetchone():
                raise ValueError(f"Response with ID '{response_id}' does not exist.")

            cur.execute(
                """
                INSERT INTO intellisupport.feedback (feedback_id, response_id, rating, comment, created_at)
                VALUES (%s, %s, %s, %s, NOW());
                """,
                (feedback_id, response_id, rating, comment)
            )
            self.conn.commit()
            
        return feedback_id

    def get_feedback_summary(self, response_id: str) -> FeedbackSummary:
        """
        Returns average rating and total feedback count for a response
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(AVG(rating), 0.0), COUNT(id)
                FROM intellisupport.feedback
                WHERE response_id = %s;
                """,
                (response_id,)
            )
            avg_rating, total_count = cur.fetchone()
            
        return FeedbackSummary(
            response_id=response_id,
            avg_rating=float(avg_rating),
            total_count=int(total_count)
        )

    def get_low_rated_responses(self, threshold: float = 2.5, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Queries responses with average feedback rating below threshold
        Returns list of dicts with keys: response_id, query_id, avg_rating, feedback_count
        Ordered by avg_rating ascending
        """
        results = []
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.response_id, r.query_id, AVG(f.rating) as avg_rating, COUNT(f.id) as feedback_count
                FROM intellisupport.feedback f
                JOIN intellisupport.responses r ON f.response_id = r.response_id
                GROUP BY f.response_id, r.query_id
                HAVING AVG(f.rating) < %s
                ORDER BY avg_rating ASC
                LIMIT %s;
                """,
                (threshold, limit)
            )
            rows = cur.fetchall()
            for row in rows:
                response_id, query_id, avg_rating, feedback_count = row
                results.append({
                    "response_id": response_id,
                    "query_id": query_id,
                    "avg_rating": float(avg_rating),
                    "feedback_count": int(feedback_count)
                })
        return results
