from typing import List
import numpy as np
import hashlib

def chunk_text(text: str, max_words: int = 300, overlap: int = 50) -> List[str]:
    """Naive word-based chunking with overlap; deterministic & dependency-light."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + max_words]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        i += max_words - overlap if max_words > overlap else max_words
    return chunks or [""]  # never return empty list

def embed_text(text: str, dim: int = 384) -> List[float]:
    """Deterministic mock embedding: seeded by blake2b hash -> normal distribution."""
    seed_bytes = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    seed = int.from_bytes(seed_bytes, "big") & 0xFFFFFFFF
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim).astype("float32")
    # L2 normalize (cosine ready)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()
