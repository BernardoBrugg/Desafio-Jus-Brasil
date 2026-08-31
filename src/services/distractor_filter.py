import re

class DistractorFilter:
    def is_header_distractor(self, start_pos: int, text: str, full_doc: str) -> bool:
        if start_pos < 220:
            header_prefix = full_doc[:start_pos].lower()
            if any(
                keyword in header_prefix
                for keyword in ["autos nº", "processo nº", "autos n.", "processo n.", "ação", "protocolo"]
            ):
                return True
        return False

    def is_meta_distractor(self, span_text: str) -> bool:
        if "PRECEDENTES INVOCADOS" in span_text:
            return True
        lower = span_text.lower()
        if re.search(r"\boab\b", lower):
            return True
        if re.search(r"\bfls?\.?\s*\d+", lower):
            return True
        if re.search(r"\bvalor\s+da\s+causa\b", lower):
            return True
        if re.search(r"\bprotocolo\b", lower):
            return True
        return False
