import unittest
from forecast import make_sales, seasonal_naive


class ForecastTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(make_sales(), make_sales())

    def test_metrics(self):
        report = seasonal_naive(make_sales())
        self.assertEqual(report["n_predictions"], 84)
        self.assertGreaterEqual(report["mae"], 0)
        self.assertGreaterEqual(report["wape"], 0)

    def test_duplicates_rejected(self):
        rows = make_sales()
        with self.assertRaises(ValueError):
            seasonal_naive(rows + [rows[0]])

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            seasonal_naive(make_sales(), holdout_days=-1)


if __name__ == "__main__":
    unittest.main()
