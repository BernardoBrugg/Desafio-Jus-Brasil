from typing import List, Optional
from pydantic import BaseModel
from src.schemas.enums import CitationType, DocumentNature
from src.schemas.citation import CitationPrediction

class DocumentInput(BaseModel):
    documento_id: str
    texto: str
    nivel: int

class DocumentOutput(BaseModel):
    documento_id: str
    citacoes: List[CitationPrediction]

class CanonicalRecord(BaseModel):
    documento_id: str
    id: int
    tribunal: Optional[str] = None
    ano: Optional[int] = None
    relator: Optional[str] = None
    natureza: DocumentNature
    tipo: CitationType
    texto: str
    texto_len: int
