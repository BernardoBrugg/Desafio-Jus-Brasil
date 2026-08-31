import json
from pathlib import Path
from typing import List
from src.schemas.document import DocumentInput, DocumentOutput
from src.schemas.citation import CitationPrediction
from src.services.extraction_service import ExtractionService
from src.services.resolution_service import ResolutionService
from src.repositories.canonical_repository import CanonicalRepository

class PipelineService:
    def __init__(self, canonical_repo: CanonicalRepository):
        self.extraction_service = ExtractionService()
        self.resolution_service = ResolutionService(canonical_repo)

    def process_document(self, document: DocumentInput) -> DocumentOutput:
        spans = self.extraction_service.extract_spans(document.texto)
        predictions: List[CitationPrediction] = []

        for span in spans:
            pred = self.resolution_service.resolve_citation(span)
            predictions.append(pred)

        return DocumentOutput(
            documento_id=document.documento_id,
            citacoes=predictions,
        )

    def save_output_json(self, output: DocumentOutput, output_dir: Path) -> Path:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"{output.documento_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output.model_dump(), f, ensure_ascii=False, indent=2)
        return file_path
