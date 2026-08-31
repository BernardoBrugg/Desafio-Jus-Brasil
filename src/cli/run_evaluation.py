import argparse
from pathlib import Path
from src.core.config import get_settings
from src.repositories.canonical_repository import CanonicalRepository
from src.repositories.document_repository import DocumentRepository
from src.repositories.goldenset_repository import GoldenSetRepository
from src.services.pipeline_service import PipelineService
from src.services.evaluation_service import EvaluationService

def run():
    settings = get_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=str(settings.input_dir))
    parser.add_argument("--db-path", type=str, default=str(settings.db_path))
    parser.add_argument("--golden-path", type=str, default=str(settings.goldenset_path))
    parser.add_argument("--min-iou", type=float, default=settings.min_iou)
    args = parser.parse_args()

    canonical_repo = CanonicalRepository(db_path=Path(args.db_path))
    doc_repo = DocumentRepository(input_dir=Path(args.input))
    golden_repo = GoldenSetRepository(file_path=Path(args.golden_path))

    pipeline = PipelineService(canonical_repo=canonical_repo)
    evaluator = EvaluationService(min_iou=args.min_iou)

    documents = doc_repo.list_all_documents()
    golden_items = golden_repo.load_items()

    predictions = [pipeline.process_document(doc) for doc in documents]
    report = evaluator.evaluate_dataset(predictions, golden_items)

    print("\n================ BENCHMARK REPORT ================")
    print(f"Overall Gold Items: {report.overall.total_gold} | Predictions: {report.overall.total_pred}")
    print(f"Span Matches (IoU >= {args.min_iou}): {report.overall.true_positives_span}")
    print(f"Span Precision: {report.overall.span_precision:.4f} | Recall: {report.overall.span_recall:.4f} | F1: {report.overall.span_f1:.4f}")
    print(f"Classification Acc: {report.overall.classification_accuracy:.4f}")
    print(f"Canonical ID Acc:   {report.overall.canonical_id_accuracy:.4f}")
    print(f"Overall Final Score:{report.overall.final_score:.4f}")
    print("--------------------------------------------------")
    for lvl, m in report.by_level.items():
        print(f"Level {lvl} (Gold={m.total_gold}, Preds={m.total_pred}):")
        print(f"  F1={m.span_f1:.4f} | ClassAcc={m.classification_accuracy:.4f} | IDAcc={m.canonical_id_accuracy:.4f}")
    print("==================================================\n")

if __name__ == "__main__":
    run()
