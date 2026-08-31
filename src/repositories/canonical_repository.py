import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set
from src.schemas.document import CanonicalRecord
from src.schemas.enums import CitationType, DocumentNature
from src.repositories.canonical_indexer import (
    extract_digits,
    extract_cnj_digits,
    extract_process_numbers,
)

class CanonicalRepository:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.records: Dict[str, CanonicalRecord] = {}
        self.cnj_to_id: Dict[str, int] = {}
        self.number_to_ids: Dict[str, Set[int]] = {}
        self._load_database()

    def _load_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT documento_id, id, tribunal, ano, relator, natureza, tipo, texto, texto_len FROM documentos"
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
            intro = rec.texto[:2000]
            cnj_list = extract_cnj_digits(intro)
            for cnj in cnj_list:
                self.cnj_to_id[cnj] = rec.id

            numbers = extract_process_numbers(intro)
            for num in numbers:
                self.number_to_ids.setdefault(num, set()).add(rec.id)

    def find_by_cnj(self, cnj_raw: str) -> Optional[int]:
        digits = extract_digits(cnj_raw)
        if not digits:
            return None
        return self.cnj_to_id.get(digits.zfill(20))

    def find_by_number(self, num_raw: str) -> List[int]:
        digits = extract_digits(num_raw)
        if not digits or len(digits) < 4:
            return []
        matched = self.number_to_ids.get(digits, set())
        return list(matched)
