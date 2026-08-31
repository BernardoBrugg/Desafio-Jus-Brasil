import re
from typing import Optional

SUMULAS_MAP = {
    ("stj", "83"): 1289710642,
    ("stj", "211"): 1289710776,
    ("stj", "443"): 1289711022,
    ("stf", "10"): 1289712966,
    ("vinculante", "10"): 1289712966,
    ("tst", "331"): 1431369957,
}

DISPOSITIVOS_MAP = {
    ("cpc", "373"): 28893055,
    ("cf", "5"): 10641516,
    ("cf", "7"): 10641213,
    ("cf", "93"): 10626510,
    ("cc", "186"): 10718759,
    ("clt", "477"): 10710324,
    ("clt", "818"): 10647746,
    ("clt", "896"): 10637358,
    ("cdc", "14"): 10606184,
    ("cpp", "312"): 10652044,
    ("cpm", "290"): 10590194,
    ("eleitoral", "276"): 10577194,
    ("lc64", "1"): 11304039,
}

class NormativeMatcher:
    def match_sumula(self, text: str) -> Optional[int]:
        lower = text.lower()
        num_match = re.search(r"\b(\d+)\b", lower)
        if not num_match:
            return None
        num = num_match.group(1)

        if "vinculante" in lower:
            return SUMULAS_MAP.get(("vinculante", num))
        for tribunal in ["stj", "stf", "tst"]:
            if tribunal in lower:
                return SUMULAS_MAP.get((tribunal, num))
        return None

    def match_dispositivo(self, text: str) -> Optional[int]:
        lower = text.lower()
        art_match = re.search(r"art(?:igo)?\.?[\s\xa0]*(\d+)", lower)
        if not art_match:
            return None
        art = art_match.group(1)

        diploma_map = [
            ("cpc", ["cpc", "processo civil"]),
            ("cf", ["cf", "constituiç", "constitucional", "república", "fedcral"]),
            ("cc", ["cc", "código civil", "codigo civil"]),
            ("clt", ["clt", "trabalho", "trabalhistas"]),
            ("cdc", ["cdc", "consumidor"]),
            ("cpp", ["cpp", "processo penal"]),
            ("cpm", ["cpm", "penal militar"]),
            ("eleitoral", ["eleitoral"]),
            ("lc64", ["lc 64", "lc64", "complementar nº 64", "inelegibilidade"]),
        ]

        for code, keys in diploma_map:
            if any(k in lower for k in keys):
                return DISPOSITIVOS_MAP.get((code, art))
        return None
