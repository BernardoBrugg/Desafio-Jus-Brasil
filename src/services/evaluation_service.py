from typing import List, Dict, Tuple, Optional
from src.schemas.document import DocumentOutput
from src.schemas.evaluation import GoldenItem, MatchMetric, EvaluationReport
from src.schemas.enums import CitationClass

class EvaluationService:
    def __init__(self, min_iou: float = 0.5):
        self.min_iou = min_iou

    def calculate_iou(self, start_a: int, end_a: int, start_b: int, end_b: int) -> float:
        intersection = max(0, min(end_a, end_b) - max(start_a, start_b))
        union = max(end_a, end_b) - min(start_a, start_b)
        return intersection / union if union > 0 else 0.0

    def evaluate_dataset(
        self,
        predictions: List[DocumentOutput],
        golden_items: List[GoldenItem],
    ) -> EvaluationReport:
        gold_by_doc: Dict[str, List[GoldenItem]] = {}
        for g in golden_items:
            gold_by_doc.setdefault(g.documento_id, []).append(g)

        pred_by_doc: Dict[str, DocumentOutput] = {p.documento_id: p for p in predictions}

        level1_gold = [g for g in golden_items if g.nivel == 1]
        level2_gold = [g for g in golden_items if g.nivel == 2]

        m1 = self._evaluate_subset(level1_gold, pred_by_doc)
        m2 = self._evaluate_subset(level2_gold, pred_by_doc)
        overall = self._evaluate_subset(golden_items, pred_by_doc)

        return EvaluationReport(
            overall=overall,
            by_level={1: m1, 2: m2},
        )

    def _evaluate_subset(
        self,
        gold_subset: List[GoldenItem],
        pred_by_doc: Dict[str, DocumentOutput],
    ) -> MatchMetric:
        if not gold_subset:
            return MatchMetric(
                total_gold=0, total_pred=0, true_positives_span=0,
                true_positives_class=0, true_positives_resolution=0,
                span_precision=0.0, span_recall=0.0, span_f1=0.0,
                classification_accuracy=0.0, canonical_id_accuracy=0.0, final_score=0.0
            )

        doc_ids = set(g.documento_id for g in gold_subset)
        subset_preds = [p for doc_id in doc_ids if doc_id in pred_by_doc for p in pred_by_doc[doc_id].citacoes]

        tp_span = 0
        tp_class = 0
        tp_res = 0

        matched_preds = set()
        for g in gold_subset:
            preds = pred_by_doc.get(g.documento_id, DocumentOutput(documento_id=g.documento_id, citacoes=[])).citacoes
            best_iou = 0.0
            best_pred = None
            best_idx = -1

            for idx, p in enumerate(preds):
                if (g.documento_id, idx) in matched_preds:
                    continue
                iou = self.calculate_iou(g.inicio, g.fim, p.inicio, p.fim)
                if iou >= self.min_iou and iou > best_iou:
                    best_iou = iou
                    best_pred = p
                    best_idx = idx

            if best_pred:
                tp_span += 1
                matched_preds.add((g.documento_id, best_idx))
                if best_pred.classificacao == g.classificacao:
                    tp_class += 1
                    if g.classificacao == CitationClass.REAL:
                        pred_id = best_pred.resolucao.id_canonico if best_pred.resolucao else None
                        if pred_id == g.id_canonico:
                            tp_res += 1
                    else:
                        tp_res += 1

        total_gold = len(gold_subset)
        total_pred = len(subset_preds)

        prec = tp_span / total_pred if total_pred > 0 else 0.0
        rec = tp_span / total_gold if total_gold > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        class_acc = tp_class / total_gold if total_gold > 0 else 0.0
        res_acc = tp_res / total_gold if total_gold > 0 else 0.0

        return MatchMetric(
            total_gold=total_gold,
            total_pred=total_pred,
            true_positives_span=tp_span,
            true_positives_class=tp_class,
            true_positives_resolution=tp_res,
            span_precision=round(prec, 4),
            span_recall=round(rec, 4),
            span_f1=round(f1, 4),
            classification_accuracy=round(class_acc, 4),
            canonical_id_accuracy=round(res_acc, 4),
            final_score=round(res_acc, 4),
        )
