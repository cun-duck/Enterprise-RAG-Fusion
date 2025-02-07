import pytest
from core.llm_integration import EnterpriseLLMEngine

class TestLLM:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.llm = EnterpriseLLMEngine()
        
    def test_generation(self):
        response = self.llm.generate("What is AI?")
        assert len(response) > 50
        assert "artificial intelligence" in response.lower()
