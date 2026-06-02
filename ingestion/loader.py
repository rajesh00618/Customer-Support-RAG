import re
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

class Document(BaseModel):
    doc_id: str
    title: str
    content: str
    source_url: Optional[str] = None
    metadata: dict = Field(default_factory=dict)

    @field_validator("doc_id")
    @classmethod
    def validate_doc_id_format(cls, v: str) -> str:
        if not re.match(r"^doc_\d{3}$", v):
            raise ValueError("doc_id must match the pattern '^doc_\\d{3}$'")
        return v

    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content must not be empty or whitespace-only")
        return v

class DocumentLoader:
    @staticmethod
    def load_from_dict(data: dict) -> Document:
        r"""
        Accepts a dictionary with keys: doc_id, title, content, source_url (optional), metadata (optional).
        Returns a Document Pydantic model.
        Must validate that doc_id matches the pattern ^doc_\d{3}$ using regex.
        Must raise ValueError if content is empty or whitespace-only.
        """
        doc_id = data.get("doc_id")
        content = data.get("content")
        
        # Explicit validation as required by method contracts
        if not doc_id or not isinstance(doc_id, str) or not re.match(r"^doc_\d{3}$", doc_id):
            raise ValueError("doc_id must match the pattern '^doc_\\d{3}$'")
        
        if not content or not isinstance(content, str) or not content.strip():
            raise ValueError("content must not be empty or whitespace-only")
            
        return Document(
            doc_id=doc_id,
            title=data.get("title", ""),
            content=content,
            source_url=data.get("source_url"),
            metadata=data.get("metadata", {})
        )

    @staticmethod
    def load_batch(data_list: list[dict]) -> list[Document]:
        """
        Calls load_from_dict for each item.
        Skips (logs warning, does not raise) any item that fails validation.
        Returns only successfully loaded documents.
        """
        loaded_docs = []
        for item in data_list:
            try:
                doc = DocumentLoader.load_from_dict(item)
                loaded_docs.append(doc)
            except Exception as e:
                logger.warning(f"Failed to load document data {item}: {e}")
        return loaded_docs

    @staticmethod
    def save_to_db(documents: list[Document], conn) -> int:
        """
        Inserts documents into intellisupport.documents.
        Uses INSERT ... ON CONFLICT (doc_id) DO UPDATE SET content = EXCLUDED.content, updated_at = NOW().
        Returns the count of rows inserted or updated.
        """
        if not documents:
            return 0
            
        import json
        affected_rows = 0
        with conn.cursor() as cur:
            for doc in documents:
                cur.execute(
                    """
                    INSERT INTO intellisupport.documents (doc_id, title, content, source_url, metadata, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (doc_id)
                    DO UPDATE SET 
                        title = EXCLUDED.title,
                        content = EXCLUDED.content,
                        source_url = EXCLUDED.source_url,
                        metadata = EXCLUDED.metadata,
                        updated_at = NOW();
                    """,
                    (
                        doc.doc_id,
                        doc.title,
                        doc.content,
                        doc.source_url,
                        json.dumps(doc.metadata),
                    )
                )
                affected_rows += cur.rowcount
            conn.commit()
        return affected_rows
