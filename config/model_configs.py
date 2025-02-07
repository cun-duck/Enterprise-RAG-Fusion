from pydantic import BaseModel

class LLMConfig(BaseModel):
    model_name: str = "meta-llama/Llama-2-70b-chat-hf"
    temperature: float = 0.3
    max_tokens: int = 512
    top_p: float = 0.9
    
class EmbeddingConfig(BaseModel):
    model_name: str = "BAAI/bge-large-en-v1.5"
    batch_size: int = 32
    normalize: bool = True
    
class RetrieverConfig(BaseModel):
    hybrid_weights: tuple = (0.7, 0.3)
    max_candidates: int = 50
    cache_ttl: int = 3600
