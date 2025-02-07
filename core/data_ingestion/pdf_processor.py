import pdfplumber
import spacy
from typing import List, Dict
from pydantic import BaseModel

class ContractClause(BaseModel):
    clause_number: str
    clause_text: str
    parties_involved: List[str]

class EnterprisePDFProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")
        
    def extract_clauses(self, file_path: str) -> List[ContractClause]:
        clauses = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                doc = self.nlp(text)
                
                current_clause = None
                for sent in doc.sents:
                    if "clause" in sent.text.lower() and any(char.isdigit() for char in sent.text):
                        if current_clause:
                            clauses.append(current_clause)
                        current_clause = ContractClause(
                            clause_number=self._extract_clause_number(sent.text),
                            clause_text=sent.text,
                            parties_involved=[]
                        )
                    elif current_clause:
                        current_clause.clause_text += " " + sent.text
                        current_clause.parties_involved.extend(
                            [ent.text for ent in sent.ents if ent.label_ in ["ORG", "PERSON"]]
                        )
        
        return clauses

    def _extract_clause_number(self, text: str) -> str:
        return ''.join(filter(str.isdigit, text))
