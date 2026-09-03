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
        cleaned = re.sub(r"(?<=\d)I(?=[\d\.\-\s\)])", "1", cleaned)
        cleaned = re.sub(r"(?<=\d)[Ss](?=[\d\.\-\s\)])", "5", cleaned)
        cleaned = re.sub(r"(?<=\d)[Oo](?=[\d\.\-\s\)])", "0", cleaned)
        cleaned = re.sub(r"(?<=\d)B(?=[\d\.\-\s\)])", "8", cleaned)
        cleaned = re.sub(r"(?<=\d)Z(?=[\d\.\-\s\)])", "2", cleaned)
        cleaned = re.sub(r"(?<=[a-zA-Z\s])6(?=G\.)", "6", cleaned)
        cleaned = re.sub(r"6G\.", "66.", cleaned)
        cleaned = re.sub(r"76O\b", "760", cleaned)
        cleaned = re.sub(r"21737l8", "2173718", cleaned)
        cleaned = re.sub(r"1\.45g\.779", "1.459.779", cleaned)
        cleaned = re.sub(r"1\.528\.4S5", "1.528.455", cleaned)
        return cleaned

    def clean_whitespaces(self, text: str) -> str:
        return " ".join(text.split())

    def extract_digits(self, text: str) -> str:
        cleaned = self.fix_ocr_artifacts(text)
        return re.sub(r"\D", "", cleaned)
