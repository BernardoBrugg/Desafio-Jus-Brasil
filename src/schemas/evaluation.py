from typing import Optional, Dict
from pydantic import BaseModel
from src.schemas.enums import CitationType, CitationClass

class GoldenItem(BaseModel):
    nivel: int
    documento_id: str
    citacao_id: str
    inicio: int
    fim: int
    trecho: str
    tipo: CitationType
    classificacao: CitationClass
    id_canonico: Optional[int] = None

class MatchMetric(BaseModel):
    total_gold: int
    total_pred: int
    true_positives_span: int
    true_positives_class: int
    true_positives_resolution: int
    span_precision: float
    span_recall: float
    span_f1: float
    classification_accuracy: float
    canonical_id_accuracy: float
    final_score: float

class EvaluationReport(BaseModel):
    overall: MatchMetric
    by_level: Dict[int, MatchMetric]
