import re

class NormalizationService:
    def fix_ocr_artifacts(self, text: str) -> str:
        cleaned = text
        cleaned = re.sub(r"\b5úmula\b", "Súmula", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b5umula\b", "Sumula", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bFedcral\b", "Federal", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bjurisprudêneia\b", "jurisprudência", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bentendirnento\b", "entendimento", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\brecentc\b", "recente", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bprofcrido\b", "proferido", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"(?<=\d)G(?=[\d\.\-\s\)])", "6", cleaned)
        cleaned = re.sub(r"(?<=\d)g(?=[\d\.\-\s\)])", "9", cleaned)
        cleaned = re.sub(r"(?<=\d)l(?=[\d\.\-\s\)])", "1", cleaned)
        cleaned = re.sub(r"(?<=\d)S(?=[\d\.\-\s\)])", "5", cleaned)
        cleaned = re.sub(r"(?<=\d)[Oo](?=[\d\.\-\s\)])", "0", cleaned)
        return cleaned

    def clean_whitespaces(self, text: str) -> str:
        return " ".join(text.split())

    def extract_digits(self, text: str) -> str:
        cleaned = self.fix_ocr_artifacts(text)
        return re.sub(r"\D", "", cleaned)
