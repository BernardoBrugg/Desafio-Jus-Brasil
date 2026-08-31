import unittest
from pathlib import Path
from src.core.config import get_settings
from src.repositories.canonical_repository import CanonicalRepository
from src.schemas.citation import ExtractedSpan
from src.schemas.enums import CitationType, CitationClass
from src.services.resolution_service import ResolutionService

class TestResolutionService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        settings = get_settings()
        cls.canonical_repo = CanonicalRepository(db_path=settings.db_path)
        cls.resolution_service = ResolutionService(canonical_repo=cls.canonical_repo)

    def test_resolve_real_acordao(self):
        span = ExtractedSpan(
            inicio=0,
            fim=30,
            trecho="RSE nº 7000592-58.2025.7.00.0000/DF",
            tipo=CitationType.JURISPRUDENCIA
        )
        pred = self.resolution_service.resolve_citation(span)
        self.assertEqual(pred.classificacao, CitationClass.REAL)
        self.assertIsNotNone(pred.resolucao)
        self.assertEqual(pred.resolucao.id_canonico, 6689204911)

    def test_resolve_inventada_acordao(self):
        span = ExtractedSpan(
            inicio=0,
            fim=25,
            trecho="Reclamação nº 66.516/RO",
            tipo=CitationType.JURISPRUDENCIA
        )
        pred = self.resolution_service.resolve_citation(span)
        self.assertEqual(pred.classificacao, CitationClass.INVENTADA)
        self.assertIsNone(pred.resolucao)

    def test_resolve_incompleta(self):
        span = ExtractedSpan(
            inicio=0,
            fim=35,
            trecho="jurisprudência pacífica desta Corte",
            tipo=CitationType.JURISPRUDENCIA
        )
        pred = self.resolution_service.resolve_citation(span)
        self.assertEqual(pred.classificacao, CitationClass.INCOMPLETA)
        self.assertIsNone(pred.resolucao)

if __name__ == "__main__":
    unittest.main()
