from enum import Enum

class CitationType(str, Enum):
    LEI = "lei"
    JURISPRUDENCIA = "jurisprudencia"

class CitationClass(str, Enum):
    REAL = "real"
    INVENTADA = "inventada"
    INCOMPLETA = "incompleta"

class DocumentNature(str, Enum):
    ACORDAO = "acordao"
    SUMULA = "sumula"
    DISPOSITIVO = "dispositivo"
