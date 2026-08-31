import unittest
from src.services.normalization_service import NormalizationService

class TestNormalizationService(unittest.TestCase):
    def setUp(self):
        self.service = NormalizationService()

    def test_ocr_artifact_cleaning(self):
        noisy = "5úmula 211 do STJ"
        cleaned = self.service.fix_ocr_artifacts(noisy)
        self.assertEqual(cleaned, "Súmula 211 do STJ")

    def test_digit_replacement_in_ocr(self):
        noisy = "Recl. n° 6G.838/BA"
        cleaned = self.service.fix_ocr_artifacts(noisy)
        self.assertEqual(cleaned, "Recl. n° 66.838/BA")

    def test_digit_extraction(self):
        raw = "REsp nº 1.741.784/PR"
        digits = self.service.extract_digits(raw)
        self.assertEqual(digits, "1741784")

    def test_whitespace_cleaning(self):
        text = "art.\n290   do   Código Penal"
        cleaned = self.service.clean_whitespaces(text)
        self.assertEqual(cleaned, "art. 290 do Código Penal")

if __name__ == "__main__":
    unittest.main()
