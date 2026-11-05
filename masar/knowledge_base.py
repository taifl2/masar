import json
from functools import lru_cache
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "certifications.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_certifications(path: Path = DATA_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cert_text(c: dict) -> str:
    return f"{c['name']} by {c['issuer']}. Skills: {', '.join(c['skills'])}"


class CertificationIndex:
    """Semantic search over the certification knowledge base."""

    def __init__(self, certifications: list[dict]):
        self.certifications = certifications
        self.by_id = {c["id"]: c for c in certifications}
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        vectors = self.embedder.encode(
            [cert_text(c) for c in certifications], normalize_embeddings=True
        )
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(np.asarray(vectors, dtype="float32"))

    def search(self, query: str, k: int = 3) -> list[tuple[dict, float]]:
        k = min(k, len(self.certifications))
        q = self.embedder.encode([query], normalize_embeddings=True)
        scores, ids = self.index.search(np.asarray(q, dtype="float32"), k)
        return [(self.certifications[i], float(s)) for i, s in zip(ids[0], scores[0])]


@lru_cache(maxsize=1)
def get_index() -> CertificationIndex:
    """Build the index once and reuse it."""
    return CertificationIndex(load_certifications())
