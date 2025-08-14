from typing import Dict, List, Any
from math import isclose

class InMemoryVectorStore:
    """
    Very simple per-document vector store; holds chunks + embeddings in memory.
    Structure: { doc_id: [ { "chunk_index": int, "text": str, "embedding": List[float] }, ... ] }
    """
    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def upsert_document(self, doc_id: str, items: List[Dict[str, Any]]) -> None:
        self._store[doc_id] = items

    def get_document(self, doc_id: str) -> List[Dict[str, Any]]:
        return self._store.get(doc_id, [])

    def delete_document(self, doc_id: str) -> None:
        self._store.pop(doc_id, None)

    def count(self, doc_id: str) -> int:
        return len(self._store.get(doc_id, []))

vector_store = InMemoryVectorStore()
