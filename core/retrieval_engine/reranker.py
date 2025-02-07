from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class CrossEncoderReranker:
    def __init__(self):
        self.model_name = "cross-encoder/ms-marco-electra-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
    def rerank(self, query: str, documents: List[str]) -> List[float]:
        features = self.tokenizer(
            [query]*len(documents),
            documents,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        
        with torch.no_grad():
            scores = self.model(**features).logits
            
        return torch.sigmoid(scores).tolist()
