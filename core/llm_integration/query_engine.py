from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Dict, Any
import torch

class EnterpriseLLMEngine:
    def __init__(self):
        self.model, self.tokenizer = self._initialize_model()
        
    def _initialize_model(self):
        model_id = "meta-llama/Llama-2-70b-chat-hf"
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            load_in_4bit=True
        )
        
        return model, tokenizer
    
    def generate_response(self, context: str, query: str) -> Dict[str, Any]:
        prompt = f"""<s>[INST] <<SYS>>
        You are an enterprise AI assistant for Fortune 500 companies. 
        Use legal and technical terminology appropriately.
        <</SYS>>

        Context: {context}

        Query: {query} [/INST]"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.3,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        return {
            "response": self.tokenizer.decode(outputs[0], skip_special_tokens=True),
            "prompt_tokens": inputs.input_ids.shape[1],
            "generated_tokens": outputs.shape[1] - inputs.input_ids.shape[1]
        }
