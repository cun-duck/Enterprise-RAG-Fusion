from fastapi import FastAPI, Security, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from core.retrieval_engine import HybridRetriever
from core.llm_integration import EnterpriseLLMEngine

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

class QueryRequest(BaseModel):
    text: str
    context: str = None

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != "supersecretkey123":
        raise HTTPException(status_code=403)
    return api_key

@app.post("/query")
async def process_query(
    request: QueryRequest,
    api_key: str = Depends(get_api_key)
):
    retriever = HybridRetriever.load_from_index()
    llm = EnterpriseLLMEngine()
    
    results = retriever.retrieve(request.text)
    context = "\n".join([res['text'] for res in results[:3]])
    
    response = llm.generate(
        context=context,
        query=request.text
    )
    
    return {
        "response": response,
        "sources": [res['metadata'] for res in results]
    }
