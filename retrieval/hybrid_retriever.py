import logging
from typing import List
from retrieval.vector_store import VectorStore, RetrievedChunk
from retrieval.bm25_retriever import BM25Retriever

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, vector_store: VectorStore, bm25_retriever: BM25Retriever, alpha: float = 0.7):
        """
        vector_store: instance of VectorStore
        bm25_retriever: instance of BM25Retriever
        alpha: weight for vector search score (1 - alpha for BM25 score)
        """
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.alpha = alpha

    def retrieve(self, query: str, query_embedding: List[float], top_k: int = 5) -> List[RetrievedChunk]:
        """
        Runs both vector search and BM25 search (each fetching top_k * 2 candidates)
        Merges results:
        - for chunks appearing in both, combines scores using: alpha * vector_score + (1 - alpha) * bm25_score
        - for chunks appearing in only one, multiplies its score by its respective weight
        Deduplicates by chunk_id
        Returns top_k results sorted by final score descending
        Sets retrieval_method = "hybrid" for merged results, "vector" or "bm25" for non-overlapping ones
        """
        candidate_k = top_k * 2
        
        # 1. Fetch candidates from both sources
        vector_candidates = self.vector_store.similarity_search(query_embedding, candidate_k)
        bm25_candidates = self.bm25_retriever.search(query, candidate_k)
        
        # Maps for quick lookup: chunk_id -> RetrievedChunk
        vector_map = {c.chunk_id: c for c in vector_candidates}
        bm25_map = {c.chunk_id: c for c in bm25_candidates}
        
        # All unique chunk IDs
        all_chunk_ids = set(vector_map.keys()).union(set(bm25_map.keys()))
        
        merged_chunks = []
        for chunk_id in all_chunk_ids:
            in_vector = chunk_id in vector_map
            in_bm25 = chunk_id in bm25_map
            
            if in_vector and in_bm25:
                # Merge scores
                v_chunk = vector_map[chunk_id]
                b_chunk = bm25_map[chunk_id]
                final_score = (self.alpha * v_chunk.score) + ((1.0 - self.alpha) * b_chunk.score)
                
                merged_chunks.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        doc_id=v_chunk.doc_id,
                        content=v_chunk.content,
                        score=final_score,
                        retrieval_method="hybrid"
                    )
                )
            elif in_vector:
                # Vector only
                v_chunk = vector_map[chunk_id]
                final_score = self.alpha * v_chunk.score
                
                merged_chunks.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        doc_id=v_chunk.doc_id,
                        content=v_chunk.content,
                        score=final_score,
                        retrieval_method="vector"
                    )
                )
            else:
                # BM25 only
                b_chunk = bm25_map[chunk_id]
                final_score = (1.0 - self.alpha) * b_chunk.score
                
                merged_chunks.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        doc_id=b_chunk.doc_id,
                        content=b_chunk.content,
                        score=final_score,
                        retrieval_method="bm25"
                    )
                )
                
        # Sort by final score descending
        merged_chunks.sort(key=lambda x: x.score, reverse=True)
        
        return merged_chunks[:top_k]

    def retrieve_with_reranking(self, query: str, query_embedding: List[float], top_k: int = 5) -> List[RetrievedChunk]:
        """
        Calls retrieve to get top_k * 3 candidates
        Reranks using a cross-encoder scoring heuristic:
        - Compute the Jaccard similarity between the query token set and each chunk's token set
        - Use this as a reranking boost: rerank_score = 0.8 * hybrid_score + 0.2 * jaccard_score
        Returns top_k after reranking
        """
        # Fetch top_k * 3 candidates
        candidates = self.retrieve(query, query_embedding, top_k * 3)
        if not candidates:
            return []
            
        query_tokens = set(query.lower().split())
        
        reranked_candidates = []
        for chunk in candidates:
            chunk_tokens = set(chunk.content.lower().split())
            
            # Compute Jaccard similarity
            intersection = query_tokens.intersection(chunk_tokens)
            union = query_tokens.union(chunk_tokens)
            jaccard_score = len(intersection) / len(union) if len(union) > 0 else 0.0
            
            # Compute reranked score
            rerank_score = (0.8 * chunk.score) + (0.2 * jaccard_score)
            
            # Update score and add to list
            chunk.score = rerank_score
            reranked_candidates.append(chunk)
            
        # Re-sort by score descending and return top_k
        reranked_candidates.sort(key=lambda x: x.score, reverse=True)
        return reranked_candidates[:top_k]
