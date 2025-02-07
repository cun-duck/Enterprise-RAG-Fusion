import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class HybridRetriever:
    def __init__(self, documents: List[str]):
        self.documents = documents
        self.encoder = SentenceTransformer("BAAI/bge-large-en-v1.5")
        self._build_indices()

    def _build_indices(self):
        # BM25 Index
        tokenized_docs = [doc.split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        # FAISS Index
        embeddings = self.encoder.encode(self.documents)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype(np.float32))
        
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        # Semantic Search
        query_embed = self.encoder.encode([query])
        D, I = self.index.search(query_embed.astype(np.float32), k)
        
        # Keyword Search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_indices = np.argsort(bm25_scores)[-k:][::-1]
        
        # Fusion
        combined_indices = list(set(I[0].tolist() + bm25_indices.tolist()))
        results = []
        for idx in combined_indices[:k]:
            results.append({
                "text": self.documents[idx],
                "score": self._calculate_fusion_score(idx, D[0], bm25_scores),
                "source": "hybrid"
            })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def _calculate_fusion_score(self, idx: int, semantic_scores: np.ndarray, bm25_scores: np.ndarray) -> float:
        norm_semantic = (semantic_scores[idx] - np.min(semantic_scores)) / (np.max(semantic_scores) - np.min(semantic_scores))
        norm_bm25 = (bm25_scores[idx] - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores))
        return 0.7 * norm_semantic + 0.3 * norm_bm25
