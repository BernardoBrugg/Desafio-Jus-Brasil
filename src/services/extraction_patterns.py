import re
from typing import List, Tuple
from src.schemas.enums import CitationType

JURIS_PATTERNS: List[Tuple[re.Pattern, CitationType]] = [
    (
        re.compile(
            r"\b(?:(?:Primeiro|Segundo|Terceiro|Quarto|Quinto)\s+)?"
            r"(?:(?:Processo|Autos)[\s\xa0]+(?:n[º°\.]*|no|n\.|n)?[\s\xa0]*)?"
            r"(?:AgR-REspe|REspe|AREspEI|R-Rp|AgR-AI|ARR|AgARR|TST-[A-Za-z0-9\-\s\.\n]+|"
            r"AgRg|AgInt|Agravo(?:\s+em|\s+de|\s+no|\s+na|\s+nos|\s+nas|\s+Interno|\s+Regimental)?|"
            r"REsp|AREsp|AgREsp|RHC|HC|MS|RMS|ADI|ADC|ADPF|RE|AI|RSE|RO|RR|AIRR|EDcl|EDs|ED|"
            r"Apelação|APL|Reclamação|Rcl|Recl\.|R\.Esp\.|Rec\.\s*Esp\.|"
            r"Recurso(?:\s+em|\s+de|\s+no|\s+na|\s+nos|\s+nas|\s+Especial|\s+Ordinário|\s+Extraordinário|\s+de\s+Revista|\s+em\s+Habeas\s+Corpus|\s+em\s+Mandado\s+de\s+Segurança)?|"
            r"Suspensão\s+de\s+Liminar\s+e\s+de\s+Sentença|SLS|"
            r"Embargos(?:\s+de\s+Declaração|\s+de\s+Divergência|\s+em|\s+nos|\s+nas)?|EREsp|EAREsp|AR)(?:\b|(?<=\.))"
            r"[^;\d]{0,80}?"
            r"(?:\d{1,7}[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}[\s\xa0\.\-]*\d[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}|"
            r"(?:\d|[lSgGOo]){1,3}(?:[\.\s\xa0\-_]+(?:\d|[lSgGOo]){2,4})+|"
            r"(?:\d|[lSgGOo]){4,8})"
            r"(?:[\s\xa0\n]*[/–\-\s\.]+[A-Z]{2}|[\s\xa0\n]*\([A-Z]{2}\))?",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:5úmula|5umula|Súmula|Súm\.|Sumula|Enunciado)[\s\xa0]+(?:Vinculante[\s\xa0]+)?(?:n[º°\.]*[\s\xa0]*)?\d+(?:[\s\xa0]+d[oa][\s\xa0]+(?:STF|STJ|TST|STM|TSE))?",
            re.IGNORECASE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:Tem[aã]|Tema)[\s\xa0]+[\d\.]+[\s\xa0]+da[\s\xa0]+repercussão[\s\xa0]+geral\b",
            re.IGNORECASE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:julgado|acórdão|precedente)[\s\xa0]+d[oa][\s\xa0]+(?:STF|STJ|TST|STM|TSE|Segunda\s+Turma|Primeira\s+Turma|Superior\s+Tribunal\s+de\s+Justiça)[^;\.]{0,180}?(?:relatoria|Rel\.|Relator|sob\s+relatoria|proferido|julgado|profcrido)[^;\.]{0,80}",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:Reclamação|Recurso\s+em\s+Habeas\s+Corpus|Agravo\s+em\s+Recurso\s+Especial|APL|Rcl)[\s\xa0]+(?:d[oa][\s\xa0]+(?:STF|STJ|TST|STM|TSE),?[\s\xa0]*)?(?:de[\s\xa0]+\d{4},?[\s\xa0]*)?Rel\.\s+(?:Min\.|Ministr[oa])[\s\xa0]+[^\n,;\.]{2,60}",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:jurisprudência\s+pacífica\s+desta\s+Corte|"
            r"entendimento\s+sumulado\s+sobre\s+a\s+matéria|"
            r"entendirnento\s+sumulado\s+sobre\s+a\s+matéria|"
            r"verbete\s+sumular\s+aplicável\s+à\s+espécie|"
            r"precedente\s+firmado\s+em\s+sede\s+de\s+recurso\s+repetitivo|"
            r"precedentes\s+desta\s+Casa\s+em\s+situações\s+análogas|"
            r"reiterados\s+precedentes\s+do\s+Superior\s+Tribunal\s+de\s+Justiça|"
            r"recente\s+acórdão\s+da\s+Segunda\s+Turma|"
            r"recentc\s+acórdão\s+da\s+Segunda\s+Turma|"
            r"orientação\s+jurisprudencial\s+da\s+Corte\s+Superior|"
            r"jurisprudência\s+consolidada\s+dos\s+tribunais\s+superiores|"
            r"jurisprudêneia\s+consolidada\s+dos\s+tribunais\s+superiores)\b",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
]

LEI_PATTERNS: List[Tuple[re.Pattern, CitationType]] = [
    (
        re.compile(
            r"\b(?:art(?:igo)?\.?[\s\xa0]*[\d\.]+[º°]?(?:[\s\xa0]*,[^\n;]{0,80})?[\s\xa0]+(?:d[oa]|de)[\s\xa0]+(?:CPC|CC|CLT|CF(?:/88)?|CPP|CPM|CDC|"
            r"Código[\s\xa0\n]+(?:de[\s\xa0\n]+Processo[\s\xa0\n]+Civil|Civil|Penal(?:[\s\xa0\n]+Militar)?|Processo[\s\xa0\n]+Penal|Defesa[\s\xa0\n]+do[\s\xa0\n]+Consumidor|Eleitoral)|"
            r"Constituição[\s\xa0\n]+(?:Federal|da[\s\xa0\n]+República|Fedcral)|"
            r"Consolidação[\s\xa0\n]+das[\s\xa0\n]+Leis[\s\xa0\n]+do[\s\xa0\n]+Trabalho|"
            r"Lei(?:[\s\xa0\n]+Complementar)?(?:[\s\xa0\n]+n[º°\.]*)?[\s\xa0\n]*[\d\./]+))",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.LEI,
    ),
    (
        re.compile(
            r"\b(?:normas?[\s\xa0\n]+de[\s\xa0\n]+regência(?:\s+da\s+matéria)?|"
            r"dispositivo[\s\xa0\n]+constitucional(?:\s+invocado\s+na\s+origem)?|"
            r"dispositivo[\s\xa0\n]+legal(?:\s+de\s+regência)?|"
            r"legislação[\s\xa0\n]+(?:de\s+regência\s+da\s+matéria|infraconstitucional\s+aplicável|aplicável)|"
            r"lei[\s\xa0\n]+que[\s\xa0\n]+disciplina[\s\xa0\n]+a[\s\xa0\n]+prescrição(?:\s+no\s+caso)?|"
            r"artigo[\s\xa0\n]+correspondente(?:[\s\xa0\n]+do[\s\xa0\n]+Código[\s\xa0\n]+de[\s\xa0\n]+Processo[\s\xa0\n]+Civil)?|"
            r"preceito[\s\xa0\n]+normativo[\s\xa0\n]+invocado)\b",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.LEI,
    ),
]
