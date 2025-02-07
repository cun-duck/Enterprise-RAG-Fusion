import spacy
from typing import List, Dict
from pydantic import BaseModel

class B2BEntity(BaseModel):
    text: str
    type: str
    start_char: int
    end_char: int

class EnterpriseEntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")
        self.entity_types = ["ORG", "PRODUCT", "CONTRACT", "CLAUSE", "VALUE"]
        
    def extract_entities(self, text: str) -> List[B2BEntity]:
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                entities.append(B2BEntity(
                    text=ent.text,
                    type=ent.label_,
                    start_char=ent.start_char,
                    end_char=ent.end_char
                ))
                
        return entities
    
    def link_entities(self, entities: List[B2BEntity]) -> Dict[str, List[str]]:
        linked = {}
        for ent in entities:
            if ent.type == "ORG":
                linked[ent.text] = self._find_related_contracts(ent.text)
        return linked
    
    def _find_related_contracts(self, org_name: str) -> List[str]:
        # Implementasi linking ke knowledge graph
        return []
