# tests/test_vector_store.py
import pytest
from app.services.vector_store import InMemoryVectorStore
from app.services.text_processing import chunk_text, embed_text

@pytest.fixture
def store():
    return InMemoryVectorStore()

def test_vector_store_upsert_get_delete(store):
    doc_id = "doc1"
    items = [{"chunk_index": 0, "text": "Hello world", "embedding": embed_text("Hello world")}]
    
    store.upsert_document(doc_id, items)
    assert store.count(doc_id) == 1

    fetched = store.get_document(doc_id)
    assert fetched[0]["text"] == "Hello world"

    store.delete_document(doc_id)
    assert store.count(doc_id) == 0

def test_chunk_text_basic():
    text = "one two three four five six seven eight nine ten"
    chunks = chunk_text(text, max_words=3, overlap=1)
    # Expect overlapping chunks of 3 words each
    assert chunks[0] == "one two three"
    assert chunks[1] == "three four five"

def test_embed_text_deterministic():
    text = "deterministic embedding"
    vec1 = embed_text(text)
    vec2 = embed_text(text)
    assert len(vec1) == len(vec2)
    # Since deterministic, vectors should be almost equal
    for a, b in zip(vec1, vec2):
        assert pytest.approx(a, rel=1e-6) == b
