import unittest
from maintenance import make_telemetry, train_logistic, probabilities, evaluate


class IndustrialRiskTests(unittest.TestCase):
    def test_reproducible_telemetry(self):
        self.assertEqual(make_telemetry(110), make_telemetry(110))

    def test_train_and_evaluate_holdout(self):
        rows = make_telemetry(150)
        model = train_logistic(rows[:120], steps=80)
        scores = probabilities(rows[120:], model)
        self.assertEqual(len(model), 5)
        self.assertEqual(len(scores), 30)
        report = evaluate(rows[120:], scores)
        for metric in ("precision", "recall", "f1", "alert_rate"):
            self.assertGreaterEqual(report[metric], 0.0)
            self.assertLessEqual(report[metric], 1.0)
        self.assertEqual(sum(report[key] for key in ("tp", "fp", "tn", "fn")), 30)

    def test_invalid_sample_size(self):
        with self.assertRaises(ValueError):
            make_telemetry(25)

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            evaluate(make_telemetry(100)[:1], [1.1])


if __name__ == "__main__":
    unittest.main()
