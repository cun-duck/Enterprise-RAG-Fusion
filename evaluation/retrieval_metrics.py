import numpy as np

class RetrievalMetrics:
    @staticmethod
    def mean_reciprocal_rank(rankings: List[int]):
        scores = []
        for rank in rankings:
            if rank == 0:
                scores.append(0)
                continue
            scores.append(1.0 / (rank + 1))
        return np.mean(scores)
    
    @staticmethod
    def normalized_dcg(scores: List[float], k: int = 10):
        def dcg(values):
            return sum([v / np.log2(i+2) for i,v in enumerate(values[:k])])
        
        ideal = sorted(scores, reverse=True)[:k]
        actual_dcg = dcg(scores)
        ideal_dcg = dcg(ideal)
        
        return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
    
    @staticmethod
    def precision_at_k(relevant: List[bool], k: int):
        return sum(relevant[:k]) / k
