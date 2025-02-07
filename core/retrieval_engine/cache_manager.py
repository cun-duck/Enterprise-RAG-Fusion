import redis
import json
from datetime import timedelta

class EnterpriseCacheManager:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.redis = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )
        
    def cache_query(self, query: str, results: List[Dict], ttl: int = 3600):
        self.redis.setex(
            f"query:{hash(query)}",
            timedelta(seconds=ttl),
            json.dumps(results)
        )
        
    def get_cached_results(self, query: str) -> List[Dict]:
        cached = self.redis.get(f"query:{hash(query)}")
        return json.loads(cached) if cached else None
