import pytest
from core.data_ingestion.pdf_processor import EnterprisePDFProcessor

class TestPDFProcessor:
    @pytest.fixture
    def processor(self):
        return EnterprisePDFProcessor()
        
    def test_contract_parsing(self, processor):
        clauses = processor.extract_clauses("sample_contract.pdf")
        assert len(clauses) > 0
        assert any(c.clause_number == "4.5" for c in clauses)
