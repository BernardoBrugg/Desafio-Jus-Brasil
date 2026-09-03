import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from src.schemas.document import CanonicalRecord
from src.schemas.enums import CitationType, DocumentNature
from src.repositories.canonical_indexer import extract_digits

class CanonicalRepository:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.records: Dict[str, CanonicalRecord] = {}
        self.primary_cnj_to_id: Dict[str, int] = {}
        self.body_cnj_to_id: Dict[str, int] = {}
        self.cnj_to_records: Dict[str, List[CanonicalRecord]] = {}
        self.number_to_records: Dict[str, List[CanonicalRecord]] = {}
        self._load_database()

    def _load_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT documento_id, id, tribunal, ano, relator, natureza, tipo, texto, texto_len FROM documentos ORDER BY id ASC"
        )
        for row in cursor.fetchall():
            rec = CanonicalRecord(
                documento_id=row[0],
                id=row[1],
                tribunal=row[2],
                ano=row[3],
                relator=row[4],
                natureza=DocumentNature(row[5]),
                tipo=CitationType(row[6]),
                texto=row[7],
                texto_len=row[8],
            )
            self.records[rec.documento_id] = rec
            self._index_record(rec)
        conn.close()

    def _index_record(self, rec: CanonicalRecord) -> None:
        if rec.natureza == DocumentNature.ACORDAO:
            header = rec.texto[:1200]
            header_matches = re.finditer(
                r"\b\d{1,7}[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}[\s\xa0\.\-]*\d[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}\b",
                header
            )
            for m in header_matches:
                d = extract_digits(m.group(0))
                if len(d) >= 15:
                    key = d.zfill(20)
                    if key not in self.primary_cnj_to_id:
                        self.primary_cnj_to_id[key] = rec.id

            body_matches = re.finditer(
                r"\b\d{1,7}[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}[\s\xa0\.\-]*\d[\s\xa0\.\-]*\d{2}[\s\xa0\.\-]*\d{4}\b",
                rec.texto
            )
            for m in body_matches:
                d = extract_digits(m.group(0))
                if len(d) >= 15:
                    key = d.zfill(20)
                    self.cnj_to_records.setdefault(key, []).append(rec)
                    if key not in self.body_cnj_to_id:
                        self.body_cnj_to_id[key] = rec.id

            intro = rec.texto[:2500]
            num_matches = re.findall(r"\b(?:\d{1,3}(?:[\.\s\xa0]\d{3})+|\d{4,8})\b", intro)
            for m in num_matches:
                d = extract_digits(m)
                if len(d) >= 4 and int(d) != 0 and not (1900 <= int(d) <= 2035):
                    existing = self.number_to_records.setdefault(d, [])
                    if not any(r.id == rec.id for r in existing):
                        existing.append(rec)

    def find_by_cnj(self, cnj_raw: str, full_citation: str = "") -> Optional[int]:
        digits = extract_digits(cnj_raw)
        if not digits:
            return None
        key = digits.zfill(20)
        if key in self.primary_cnj_to_id:
            return self.primary_cnj_to_id[key]
        recs = self.cnj_to_records.get(key, [])
        if recs:
            if len(recs) == 1:
                return recs[0].id
            if "agarr" in full_citation.lower():
                for r in recs:
                    if "agarr" in r.texto[:400].lower() or "agravo da reclamante" in r.texto[:400].lower() or "recurso de revista com agravo" in r.texto[:400].lower():
                        return r.id
            return recs[0].id
        return self.body_cnj_to_id.get(key)

    def find_by_number(self, num_raw: str, tribunal_hint: Optional[str] = None, appeal_hint: Optional[str] = None) -> List[int]:
        digits = extract_digits(num_raw)
        if not digits or len(digits) < 4:
            return []
        recs = self.number_to_records.get(digits, [])
        if not recs:
            return []
        
        candidates = recs
        if tribunal_hint:
            filtered = [r for r in candidates if r.tribunal and r.tribunal.upper() == tribunal_hint.upper()]
            if filtered:
                candidates = filtered

        if len(candidates) > 1 and appeal_hint:
            if appeal_hint == "recurso especial":
                resp_candidates = [r for r in candidates if "embargos de divergência" not in r.texto[:300].lower()]
                if resp_candidates:
                    candidates = resp_candidates

        seen = []
        for r in candidates:
            if r.id not in seen:
                seen.append(r.id)
        return seen
