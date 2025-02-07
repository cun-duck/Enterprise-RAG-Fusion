import pytest
from core.knowledge_graph.entity_extractor import EnterpriseEntityExtractor

class TestEntityExtractor:
    @pytest.fixture
    def extractor(self):
        return EnterpriseEntityExtractor()
        
    def test_entity_extraction(self, extractor):
        text = "Vendor X agrees to deliver according to Contract Y-2024"
        entities = extractor.extract_entities(text)
        assert len(entities) >= 2
        assert any(e.type == "ORG" for e in entities)
