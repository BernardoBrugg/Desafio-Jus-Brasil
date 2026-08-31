import re
from typing import List, Set

def extract_digits(text: str) -> str:
    return re.sub(r"\D", "", text)

def extract_cnj_digits(text: str) -> List[str]:
    matches = re.findall(r"\b\d{1,7}[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}[\s\xa0\.\-]*\d[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}\b", text)
    result = []
    for m in matches:
        digits = extract_digits(m)
        if len(digits) >= 15:
            result.append(digits.zfill(20))
    return result

def extract_process_numbers(text: str) -> Set[str]:
    numbers = set()
    matches = re.findall(r"\b(?:\d{1,3}(?:[\.\s\xa0]\d{3})+|\d{4,8})\b", text)
    for m in matches:
        digits = extract_digits(m)
        if len(digits) >= 4 and not (1990 <= int(digits) <= 2030):
            numbers.add(digits)
    return numbers
