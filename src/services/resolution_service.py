import re
from typing import Optional, List
from src.schemas.citation import ExtractedSpan, CitationPrediction, Resolution
from src.schemas.enums import CitationClass, CitationType
from src.repositories.canonical_repository import CanonicalRepository
from src.services.normalization_service import NormalizationService
from src.services.normative_matcher import NormativeMatcher

def is_calendar_year(num_str: str) -> bool:
    if len(num_str) == 4 and num_str.isdigit():
        val = int(num_str)
        return 1900 <= val <= 2035
    return False

class ResolutionService:
    def __init__(self, canonical_repo: CanonicalRepository):
        self.canonical_repo = canonical_repo
        self.normalization_service = NormalizationService()
        self.normative_matcher = NormativeMatcher()

    def resolve_citation(self, span: ExtractedSpan) -> CitationPrediction:
        cleaned_text = self.normalization_service.fix_ocr_artifacts(span.trecho)
        if span.tipo == CitationType.LEI:
            return self._resolve_lei(span, cleaned_text)
        return self._resolve_jurisprudencia(span, cleaned_text)

    def _resolve_lei(self, span: ExtractedSpan, text: str) -> CitationPrediction:
        lower = text.lower()
        if any(g in lower for g in ["normas", "regência", "dispositivo constitucional", "dispositivo legal", "legislação", "prescrição", "artigo correspondente", "preceito normativo"]):
            return CitationPrediction(
                inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                tipo=span.tipo, classificacao=CitationClass.INCOMPLETA, resolucao=None
            )

        match_id = self.normative_matcher.match_dispositivo(text)
        if match_id:
            return CitationPrediction(
                inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                tipo=span.tipo, classificacao=CitationClass.REAL,
                resolucao=Resolution(id_canonico=match_id)
            )
        return CitationPrediction(
            inicio=span.inicio, fim=span.fim, trecho=span.trecho,
            tipo=span.tipo, classificacao=CitationClass.INVENTADA, resolucao=None
        )

    def _resolve_jurisprudencia(self, span: ExtractedSpan, text: str) -> CitationPrediction:
        lower = text.lower()
        if any(g in lower for g in ["julgado do", "acórdão do", "precedente do", "precedente firmado", "precedentes", "jurisprudência", "entendimento", "orientação", "verbete sumular", "recente acórdão", "recentc acórdão", "temã", "tema", "reiterados"]):
            raw_nums = re.findall(r"\b(?:\d{1,3}(?:[\.\s\xa0]\d{3})+|\d{4,8})\b", text)
            non_years = [n for n in raw_nums if not is_calendar_year(re.sub(r"\D", "", n))]
            if not non_years and not re.search(r"\d{4}\.\d", text):
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.INCOMPLETA, resolucao=None
                )

        if "súmula" in lower or "sumula" in lower or "súm." in lower:
            sumula_id = self.normative_matcher.match_sumula(text)
            if sumula_id:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.REAL,
                    resolucao=Resolution(id_canonico=sumula_id)
                )
            return CitationPrediction(
                inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                tipo=span.tipo, classificacao=CitationClass.INVENTADA, resolucao=None
            )

        cnj_digits = self.normalization_service.extract_digits(text)
        if len(cnj_digits) >= 15:
            cnj_id = self.canonical_repo.find_by_cnj(cnj_digits, full_citation=text)
            if cnj_id:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.REAL,
                    resolucao=Resolution(id_canonico=cnj_id)
                )
            return CitationPrediction(
                inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                tipo=span.tipo, classificacao=CitationClass.INVENTADA, resolucao=None
            )

        tribunal_hint = None
        if "stj" in lower or "recurso especial" in lower or "resp" in lower or "aresp" in lower:
            tribunal_hint = "STJ"
        elif "stf" in lower or "recurso extraordinário" in lower or "re " in lower:
            tribunal_hint = "STF"
        elif "tst" in lower:
            tribunal_hint = "TST"
        elif "stm" in lower:
            tribunal_hint = "STM"
        elif "tse" in lower:
            tribunal_hint = "TSE"

        appeal_hint = None
        if "embargos de divergência" in lower or "eresp" in lower:
            appeal_hint = "embargos de divergência"
        elif "recurso especial" in lower or "resp" in lower:
            appeal_hint = "recurso especial"

        raw_candidates = re.findall(r"\b(?:\d{1,3}(?:[\.\s\xa0]\d{3})+|\d{4,8})\b", text)
        candidate_nums = [
            self.normalization_service.extract_digits(c)
            for c in raw_candidates
            if not is_calendar_year(self.normalization_service.extract_digits(c))
        ]

        for cand in candidate_nums:
            matched_ids = self.canonical_repo.find_by_number(cand, tribunal_hint=tribunal_hint, appeal_hint=appeal_hint)
            if len(matched_ids) == 1:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.REAL,
                    resolucao=Resolution(id_canonico=matched_ids[0])
                )
            elif len(matched_ids) > 1:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.INCOMPLETA, resolucao=None
                )

        digits = self.normalization_service.extract_digits(text)
        if len(digits) >= 4 and not is_calendar_year(digits):
            matched_ids = self.canonical_repo.find_by_number(digits, tribunal_hint=tribunal_hint, appeal_hint=appeal_hint)
            if len(matched_ids) == 1:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.REAL,
                    resolucao=Resolution(id_canonico=matched_ids[0])
                )
            elif len(matched_ids) > 1:
                return CitationPrediction(
                    inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                    tipo=span.tipo, classificacao=CitationClass.INCOMPLETA, resolucao=None
                )
            return CitationPrediction(
                inicio=span.inicio, fim=span.fim, trecho=span.trecho,
                tipo=span.tipo, classificacao=CitationClass.INVENTADA, resolucao=None
            )

        return CitationPrediction(
            inicio=span.inicio, fim=span.fim, trecho=span.trecho,
            tipo=span.tipo, classificacao=CitationClass.INCOMPLETA, resolucao=None
        )
