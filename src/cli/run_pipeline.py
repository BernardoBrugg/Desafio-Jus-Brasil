import argparse
from pathlib import Path
from src.core.config import get_settings
from src.repositories.canonical_repository import CanonicalRepository
from src.repositories.document_repository import DocumentRepository
from src.services.pipeline_service import PipelineService

def run():
    settings = get_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=str(settings.input_dir))
    parser.add_argument("--output", type=str, default=str(settings.output_dir))
    parser.add_argument("--db-path", type=str, default=str(settings.db_path))
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    db_path = Path(args.db_path)

    canonical_repo = CanonicalRepository(db_path=db_path)
    doc_repo = DocumentRepository(input_dir=input_dir)
    pipeline = PipelineService(canonical_repo=canonical_repo)

    documents = doc_repo.list_all_documents()
    print(f"Loaded {len(documents)} documents from {input_dir}")

    for doc in documents:
        output = pipeline.process_document(doc)
        out_file = pipeline.save_output_json(output, output_dir)
        print(f"Saved: {out_file.name} ({len(output.citacoes)} citations)")

if __name__ == "__main__":
    run()
