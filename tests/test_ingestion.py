import os
import pytest
import psycopg2
from config import settings
from ingestion.loader import DocumentLoader, Document
from ingestion.chunker import DocumentChunker, Chunk
from ingestion.embedder import Embedder, EmbeddingError

# Helper fixture for DB connection
@pytest.fixture(scope="module")
def conn():
    connection = psycopg2.connect(settings.database_url)
    yield connection
    connection.rollback()
    connection.close()

# Helper decorator to skip OpenAI calls if no key is configured
openai_test = pytest.mark.skipif(
    settings.openai_api_key in ("your-openai-api-key-here", "your-nvidia-api-key-here")
    or not (settings.openai_api_key.startswith("sk-") or settings.openai_api_key.startswith("nvapi-")),
    reason="Requires a valid OpenAI/NVIDIA API key"
)

def test_load_from_dict_valid():
    data = {
        "doc_id": "doc_001",
        "title": "Getting Started with Nexora",
        "content": "This is a valid support document with enough words.",
        "source_url": "https://docs.nexora.com/intro",
        "metadata": {"category": "onboarding"}
    }
    doc = DocumentLoader.load_from_dict(data)
    assert doc.doc_id == "doc_001"
    assert doc.title == "Getting Started with Nexora"
    assert doc.content == "This is a valid support document with enough words."
    assert doc.source_url == "https://docs.nexora.com/intro"
    assert doc.metadata == {"category": "onboarding"}

def test_load_from_dict_invalid_doc_id():
    data = {
        "doc_id": "document_1",
        "title": "Invalid ID Document",
        "content": "This has an invalid ID pattern."
    }
    with pytest.raises(ValueError) as excinfo:
        DocumentLoader.load_from_dict(data)
    assert "doc_id" in str(excinfo.value)

def test_load_from_dict_empty_content():
    data = {
        "doc_id": "doc_001",
        "title": "Empty Content Document",
        "content": "   "
    }
    with pytest.raises(ValueError) as excinfo:
        DocumentLoader.load_from_dict(data)
    assert "content" in str(excinfo.value)

def test_chunk_document_chunk_ids():
    doc = Document(
        doc_id="doc_001",
        title="Test Doc",
        content="Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9 Word10"
    )
    chunker = DocumentChunker(chunk_size=5, chunk_overlap=2)
    chunks = chunker.chunk_document(doc)
    
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.chunk_id.startswith("chunk_doc_001_")
        assert chunk.doc_id == "doc_001"

def test_chunk_overlap():
    doc = Document(
        doc_id="doc_002",
        title="Test Doc Overlap",
        content="A B C D E F G H I J K L M N O"
    )
    # chunk_size = 10, overlap = 3. 
    # Chunk 0: A B C D E F G H I J (index 0 to 9)
    # Chunk 1 starts at 10 - 3 = 7. 
    # Chunk 1: H I J K L M N O (index 7 to 14)
    # Overlap is H I J
    chunker = DocumentChunker(chunk_size=10, chunk_overlap=3)
    chunks = chunker.chunk_document(doc)
    
    assert len(chunks) == 2
    assert chunks[0].content == "A B C D E F G H I J"
    assert chunks[1].content == "H I J K L M N O"
    
    # Assert overlapping content is shared
    assert "H I J" in chunks[0].content
    assert chunks[1].content.startswith("H I J")

@openai_test
def test_embed_text_shape():
    embedder = Embedder()
    embedding = embedder.embed_text("Sample support query")
    assert isinstance(embedding, list)
    assert len(embedding) == 1024
    for val in embedding:
        assert isinstance(val, float)
