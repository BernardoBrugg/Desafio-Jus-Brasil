import re
from typing import List, Tuple
from src.schemas.enums import CitationType

UF_LIST = "AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO"

ORDINAL_PREFIX = r"(?:(?:Primeir[oa]|Segund[oa]|Terceir[oa]|Quart[oa]|Quint[oa]|1[º°ª]|2[º°ª]|3[º°ª])[\s\xa0\n]+)?"
PROCESS_WRAPPER = r"(?:(?:Processo|Autos)[\s\xa0\n]+(?:n[º°\.]*|no|n\.|n)?[\s\xa0\n]*)?"
COURT_PREFIX = r"(?:(?:TST|STF|STJ|STM|TSE)[\s\xa0\n\-_]+)?"
CHAINED_APPEAL_PREFIX = r"(?:(?:(?:ED(?:cl|s)?|AgR(?:-AI|-REspe)?|Ag(?:ravo)?(?:\s+em|\s+de|\s+no|\s+na|\s+nos|\s+nas|\s+Interno|\s+Regimental|\s+de\s+Instrumento|\.?(?:\s*Reg|\s*Int)\.?)?|EAREsp|EREsp|E-ED|ED-E-ED)[\s\xa0\n\-_]+(?:em|no|na|nos|nas|n[º°\.]*)?[\s\xa0\n\-_]*)*)"
MAIN_APPEAL_TYPE = (
    r"(?:AgR-REspe|REspe\.?|AREspEI|R-Rp|AgR-AI|ARR|AgARR|AIRR|AgRg|AgInt|Ag\.?\s*Int\.?|AG\.?REG|Ag\.?\s*Reg\.?|"
    r"Agravo(?:\s+em|\s+de|\s+no|\s+na|\s+nos|\s+nas|\s+Interno|\s+Regimental|\s+de\s+Instrumento|\.?(?:\s*Reg|\s*Int)\.?)?|"
    r"REsp|AREsp|A\.?\s*REsp|AgREsp|RHC|HC|H\.C\.|MS|RMS|ADI|ADC|ADPF|RE\.?|AI|RSE|RO|RR|RRAg|AIRR|EDcl|EDs|ED|Apelação|APL|"
    r"Reclamação|Rcl|Recl\.|RCL|R\.?Esp\.?|Rec\.\s*Esp\.?|"
    r"Recurso[\s\xa0\n]+(?:em[\s\xa0\n]+|de[\s\xa0\n]+|no[\s\xa0\n]+|na[\s\xa0\n]+|nos[\s\xa0\n]+|nas[\s\xa0\n]+|Especial(?:[\s\xa0\n]+Eleitoral)?|Ordinário|Extraordinário(?:[\s\xa0\n]+com[\s\xa0\n]+Agravo)?|de[\s\xa0\n]+Revista|em[\s\xa0\n]+Habeas[\s\xa0\n]+Corpus|em[\s\xa0\n]+Mandado[\s\xa0\n]+de[\s\xa0\n]+Segurança|Eleitoral)|"
    r"Suspensão[\s\xa0\n]+de[\s\xa0\n]+(?:Liminar[\s\xa0\n]+e[\s\xa0\n]+de[\s\xa0\n]+Sentença|Segurança|Liminar)|SLS|SL|SS|STA|STP|"
    r"Embargos[\s\xa0\n]+(?:de[\s\xa0\n]+Declaração|de[\s\xa0\n]+Divergência|em|nos|nas)?|EREsp|EAREsp|AR|"
    r"Pet|Petição|Conflito[\s\xa0\n]+de[\s\xa0\n]+Competência|Mandado[\s\xa0\n]+de[\s\xa0\n]+Injunção|MI|"
    r"Ação[\s\xa0\n]+(?:Rescisória|Penal|Direta[\s\xa0\n]+de[\s\xa0\n]+Inconstitucionalidade|Civil[\s\xa0\n]+Pública)|ACP|"
    r"ArgInc|Arguição[\s\xa0\n]+de[\s\xa0\n]+(?:Inconstitucionalidade|Descumprimento[\s\xa0\n]+de[\s\xa0\n]+Preceito[\s\xa0\n]+Fundamental)|IRDR|IAC)"
)
NUMBER_CONNECTOR = r"[\s\xa0\n\-_]*(?:n[º°\.]*|no|n\.|n|número|sob[\s\xa0\n]+o[\s\xa0\n]+n[º°\.]*)?[\s\xa0\n\-_]*"
NUMBER_PATTERN = r"(?:\d{1,7}[\s\xa0\.\-_]*\d{2}[\s\xa0\.\-_]*\d{4}[\s\xa0\.\-_]*\d[\s\xa0\.\-_]*\d{2}[\s\xa0\.\-_]*\d{4}|\d{7}[\s\xa0\.\-_]+\d{13}|\d{7}[\s\xa0\.\-_]+\d{2}[\s\xa0\.\-_]*\d{11}|\d{15,20}|(?:\d|[lSgGOo]){0,4}\d(?:\d|[lSgGOo]){0,4}(?:[\.\s\xa0\-_]+(?:\d|[lSgGOo])+)*(?!\d|[lSgGOo]))"
UF_SUFFIX = rf"(?:[\s\xa0\n]*[/–\-\s\.]+(?:{UF_LIST})|[\s\xa0\n]*\((?:{UF_LIST})\))?"

JURIS_PATTERNS: List[Tuple[re.Pattern, CitationType]] = [
    (
        re.compile(
            rf"\b{ORDINAL_PREFIX}{PROCESS_WRAPPER}{COURT_PREFIX}(?:{CHAINED_APPEAL_PREFIX}{MAIN_APPEAL_TYPE})(?:\b|(?<=\.)){NUMBER_CONNECTOR}{NUMBER_PATTERN}{UF_SUFFIX}",
            re.IGNORECASE | re.MULTILINE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:5úmula|5umula|Súmula|Súm\.|Sumula|Enunciado)[\s\xa0\n]+(?:Vinculante[\s\xa0\n]+)?(?:n[º°\.]*[\s\xa0\n]*)?\d+(?:[\s\xa0\n]+d[oa][\s\xa0\n]+(?:STF|STJ|TST|STM|TSE))?",
            re.IGNORECASE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:Tem[aã]|Tema)[\s\xa0\n]+[\d\.]+[\s\xa0\n]+da[\s\xa0\n]+repercussão[\s\xa0\n]+geral\b",
            re.IGNORECASE,
        ),
        CitationType.JURISPRUDENCIA,
    ),
    (
        re.compile(
            r"\b(?:"
            r"(?:julgado|acórdão|precedente)[\s\xa0\n]+d[oa][\s\xa0\n]+(?:STF|STJ|TST|STM|TSE|Segunda\s+Turma|Primeira\s+Turma|Superior\s+Tribunal\s+de\s+Justiça)|"
            r"(?:Reclamação|Recurso[\s\xa0\n]+(?:em[\s\xa0\n]+Habeas[\s\xa0\n]+Corpus|Especial|Extraordinário|Ordinário)|Agravo[\s\xa0\n]+em[\s\xa0\n]+Recurso[\s\xa0\n]+Especial|APL|Rcl)"
            r"(?:[\s\xa0\n]+d[oa][\s\xa0\n]+(?:STF|STJ|TST|STM|TSE))?"
            r")"
            r"[\s\xa0\n,]+(?:de[\s\xa0\n]+\d{4}[\s\xa0\n,]+|(?:julgado|proferido|profcrido)[\s\xa0\n]+(?:em[\s\xa0\n]+\d{4}[\s\xa0\n]+)?)*"
            r"(?:da[\s\xa0\n]+relatoria[\s\xa0\n]+d[eoa]|sob[\s\xa0\n]+relatoria[\s\xa0\n]+d[eoa]|pela[\s\xa0\n]+relatoria[\s\xa0\n]+d[eoa]|pela[\s\xa0\n]+relatoria[\s\xa0\n]+dc|Rel\.|Relator|Relatora)"
            r"(?:[\s\xa0\n]+(?:Min\.|Ministr[oa]\.?))?[\s\xa0\n]+"
            r"[A-ZÀ-Úa-zà-ú]+(?:\s+[A-ZÀ-Úa-zà-ú]+){1,5}\b",
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
            r"precedente\s+firmado[\s\n]+em\s+sede\s+de\s+recurso\s+repetitivo|"
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
            r"\b(?:art(?:igo)?\.?[\s\xa0\n]*[\d\.]+[º°]?(?:[\s\xa0\n]*,[^\n;]{0,80})?[\s\xa0\n]+(?:d[oa]|de)[\s\xa0\n]+(?:CPC|CC|CLT|CF(?:/88)?|CPP|CPM|CDC|CTN|ECA|LIA|"
            r"Código[\s\xa0\n]+(?:de[\s\xa0\n]+Processo[\s\xa0\n]+Civil|Civil|Penal(?:[\s\xa0\n]+Militar)?|de[\s\xa0\n]+Processo[\s\xa0\n]+Penal|Processo[\s\xa0\n]+Penal|de[\s\xa0\n]+Defesa[\s\xa0\n]+do[\s\xa0\n]+Consumidor|Defesa[\s\xa0\n]+do[\s\xa0\n]+Consumidor|Eleitoral|Tributário[\s\xa0\n]+Nacional)|"
            r"Estatuto[\s\xa0\n]+(?:da[\s\xa0\n]+Criança[\s\xa0\n]+e[\s\xa0\n]+do[\s\xa0\n]+Adolescente|da[\s\xa0\n]+OAB|da[\s\xa0\n]+Cidade|do[\s\xa0\n]+Idoso)|"
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
