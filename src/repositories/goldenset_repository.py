import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional
from src.schemas.evaluation import GoldenItem
from src.schemas.enums import CitationType, CitationClass
from src.core.exceptions import InvalidGoldenSetError

class GoldenSetRepository:
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)

    def _extract_shared_strings(self, zip_ref: zipfile.ZipFile) -> List[str]:
        strings = []
        if "xl/sharedStrings.xml" in zip_ref.namelist():
            tree = ET.fromstring(zip_ref.read("xl/sharedStrings.xml"))
            for elem in tree.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
                t = elem.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                strings.append(t.text if t is not None and t.text else "")
        return strings

    def load_items(self) -> List[GoldenItem]:
        if not self.file_path.exists():
            raise InvalidGoldenSetError(f"Golden set file not found: {self.file_path}")

        items = []
        with zipfile.ZipFile(self.file_path) as zip_ref:
            shared_strings = self._extract_shared_strings(zip_ref)
            sheet_tree = ET.fromstring(zip_ref.read("xl/worksheets/sheet1.xml"))
            rows_elem = sheet_tree.findall(
                "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetData/{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"
            )

            for index, row in enumerate(rows_elem):
                if index == 0:
                    continue
                
                cells = []
                for cell in row.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
                    v = cell.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                    t = cell.attrib.get("t")
                    val = v.text if v is not None else ""
                    if t == "s" and val and int(val) < len(shared_strings):
                        val = shared_strings[int(val)]
                    cells.append(val)

                if len(cells) < 8:
                    continue

                raw_id_canonico = cells[8] if len(cells) > 8 and cells[8] else None
                id_canonico = int(float(raw_id_canonico)) if raw_id_canonico else None

                items.append(
                    GoldenItem(
                        nivel=int(float(cells[0])),
                        documento_id=cells[1].strip(),
                        citacao_id=cells[2].strip(),
                        inicio=int(float(cells[3])),
                        fim=int(float(cells[4])),
                        trecho=cells[5].replace("\\n", "\n"),
                        tipo=CitationType(cells[6].strip()),
                        classificacao=CitationClass(cells[7].strip()),
                        id_canonico=id_canonico,
                    )
                )
        return items
