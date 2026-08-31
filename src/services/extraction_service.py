from typing import List
from src.schemas.citation import ExtractedSpan
from src.schemas.enums import CitationType
from src.services.distractor_filter import DistractorFilter
from src.services.extraction_patterns import JURIS_PATTERNS, LEI_PATTERNS

class ExtractionService:
    def __init__(self):
        self.distractor_filter = DistractorFilter()

    def extract_spans(self, text: str) -> List[ExtractedSpan]:
        candidates: List[ExtractedSpan] = []

        all_patterns = JURIS_PATTERNS + LEI_PATTERNS
        for pattern, cit_type in all_patterns:
            for match in pattern.finditer(text):
                start, end = match.span()
                span_text = text[start:end]

                if self.distractor_filter.is_header_distractor(start, span_text, text):
                    continue
                if self.distractor_filter.is_meta_distractor(span_text):
                    continue

                candidates.append(
                    ExtractedSpan(
                        inicio=start,
                        fim=end,
                        trecho=span_text,
                        tipo=cit_type,
                    )
                )

        return self._resolve_overlapping_spans(candidates)

    def _resolve_overlapping_spans(self, spans: List[ExtractedSpan]) -> List[ExtractedSpan]:
        if not spans:
            return []

        sorted_spans = sorted(spans, key=lambda s: (s.inicio, -(s.fim - s.inicio)))
        resolved: List[ExtractedSpan] = []

        for current in sorted_spans:
            if not resolved:
                resolved.append(current)
                continue

            last = resolved[-1]
            if current.inicio < last.fim:
                if (current.fim - current.inicio) > (last.fim - last.inicio):
                    resolved[-1] = current
            else:
                resolved.append(current)

        return resolved
