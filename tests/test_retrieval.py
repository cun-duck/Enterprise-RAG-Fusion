import pytest
from core.retrieval_engine import HybridRetriever

@pytest.fixture
def sample_docs():
    return [
        "Vendor X agrees to provide services per SLA section 4.5",
        "Meeting minutes from 2024-01-15 discuss Q2 deliverables",
        "CRM data shows Vendor X performance at 98.3%"
    ]

def test_hybrid_retrieval(sample_docs):
    retriever = HybridRetriever(sample_docs)
    results = retriever.retrieve("SLA terms with Vendor X")
    assert len(results) > 0
    assert "SLA" in results[0]['text']
