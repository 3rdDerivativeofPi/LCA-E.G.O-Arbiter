import numpy as np
import faiss


class VectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine on normalized vectors)
        self.metadata = []  # Store candidate info alongside vectors

    def _normalize(self, vector: list[float]) -> np.ndarray:
        v = np.array(vector, dtype=np.float32)
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def add(self, vector: list[float], meta: dict):
        v = self._normalize(vector).reshape(1, -1)
        self.index.add(v) # type: ignore
        self.metadata.append(meta)

    def search(self, vector: list[float], top_k: int = 5) -> list[dict]:
        v = self._normalize(vector).reshape(1, -1)
        scores, indices = self.index.search(v, top_k) # type: ignore
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "score": round(float(score) * 100, 2),
                "meta": self.metadata[idx]
            })
        return results

    def clear(self):
        self.index.reset()
        self.metadata = []


# Singleton
vector_store = VectorStore()