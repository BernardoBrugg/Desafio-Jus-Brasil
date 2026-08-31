import unittest
from src.schemas.enums import CitationType, CitationClass
from src.schemas.citation import CitationPrediction, Resolution, ExtractedSpan
from src.schemas.document import DocumentInput, DocumentOutput

class TestSchemas(unittest.TestCase):
    def test_extracted_span(self):
        span = ExtractedSpan(
            inicio=0,
            fim=25,
            trecho="REsp nº 1.741.784/PR",
            tipo=CitationType.JURISPRUDENCIA
        )
        self.assertEqual(span.inicio, 0)
        self.assertEqual(span.fim, 25)
        self.assertEqual(span.tipo, CitationType.JURISPRUDENCIA)

    def test_citation_prediction_serialization(self):
        pred = CitationPrediction(
            inicio=10,
            fim=30,
            trecho="art. 373, I, do CPC",
            tipo=CitationType.LEI,
            classificacao=CitationClass.REAL,
            resolucao=Resolution(id_canonico=28893055)
        )
        data = pred.model_dump()
        self.assertEqual(data["inicio"], 10)
        self.assertEqual(data["tipo"], "lei")
        self.assertEqual(data["classificacao"], "real")
        self.assertEqual(data["resolucao"]["id_canonico"], 28893055)

    def test_document_output_structure(self):
        output = DocumentOutput(
            documento_id="gen_n1_001",
            citacoes=[]
        )
        self.assertEqual(output.documento_id, "gen_n1_001")
        self.assertEqual(len(output.citacoes), 0)

if __name__ == "__main__":
    unittest.main()
