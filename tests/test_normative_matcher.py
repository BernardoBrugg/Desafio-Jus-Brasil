import unittest
from src.services.normative_matcher import NormativeMatcher

class TestNormativeMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = NormativeMatcher()

    def test_match_sumula_vinculante(self):
        matched_id = self.matcher.match_sumula("Súmula Vinculante 10")
        self.assertEqual(matched_id, 1289712966)

    def test_match_sumula_stj(self):
        matched_id = self.matcher.match_sumula("Súmula 83 do STJ")
        self.assertEqual(matched_id, 1289710642)

    def test_match_dispositivo_cpc(self):
        matched_id = self.matcher.match_dispositivo("art. 373, I, do CPC")
        self.assertEqual(matched_id, 28893055)

    def test_match_dispositivo_cf(self):
        matched_id = self.matcher.match_dispositivo("artigo 5º da Constituição Federal")
        self.assertEqual(matched_id, 10641516)

    def test_unmatched_sumula(self):
        matched_id = self.matcher.match_sumula("Súmula 999 do STJ")
        self.assertIsNone(matched_id)

if __name__ == "__main__":
    unittest.main()
