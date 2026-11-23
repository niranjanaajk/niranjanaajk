import unittest
from risk import make_transactions, evaluate_triage, risk_score


class RiskTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(make_transactions(100), make_transactions(100))

    def test_score_range(self):
        for record in make_transactions(100):
            self.assertTrue(0 <= risk_score(record) <= 1)

    def test_evaluation(self):
        report = evaluate_triage(make_transactions(120))
        self.assertEqual(report["transactions"], 120)
        self.assertGreaterEqual(report["recall"], 0)

    def test_duplicates(self):
        records = make_transactions(5)
        with self.assertRaises(ValueError):
            evaluate_triage(records + [records[0]])


if __name__ == "__main__":
    unittest.main()
