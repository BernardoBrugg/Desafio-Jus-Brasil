from pathlib import Path
from typing import List
from src.schemas.document import DocumentInput
from src.core.exceptions import DocumentNotFoundError

class DocumentRepository:
    def __init__(self, input_dir: Path):
        self.input_dir = Path(input_dir)

    def get_document(self, documento_id: str) -> DocumentInput:
        file_path = self.input_dir / f"{documento_id}.txt"
        if not file_path.exists():
            raise DocumentNotFoundError(f"Document file not found: {file_path}")
        
        texto = file_path.read_text(encoding="utf-8")
        nivel = 2 if "n2" in documento_id else 1
        return DocumentInput(documento_id=documento_id, texto=texto, nivel=nivel)

    def list_all_documents(self) -> List[DocumentInput]:
        if not self.input_dir.exists():
            return []
        
        documents = []
        for file_path in sorted(self.input_dir.glob("*.txt")):
            documento_id = file_path.stem
            texto = file_path.read_text(encoding="utf-8")
            nivel = 2 if "n2" in documento_id else 1
            documents.append(
                DocumentInput(documento_id=documento_id, texto=texto, nivel=nivel)
            )
        return documents
