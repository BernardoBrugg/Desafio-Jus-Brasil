from typing import Optional
from pydantic import BaseModel, Field
from src.schemas.enums import CitationType, CitationClass

class Resolution(BaseModel):
    id_canonico: Optional[int] = None

class CitationPrediction(BaseModel):
    inicio: int
    fim: int
    trecho: str
    tipo: CitationType
    classificacao: CitationClass
    resolucao: Optional[Resolution] = None
    confianca: Optional[float] = Field(default=None, ge=0.0, le=1.0)

class ExtractedSpan(BaseModel):
    inicio: int
    fim: int
    trecho: str
    tipo: CitationType
    is_distractor: bool = False
