import unittest
from churn import demo_subscribers, segment_summary


class ChurnTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(demo_subscribers(30), demo_subscribers(30))

    def test_all_customers_accounted_for(self):
        rows = demo_subscribers(100)
        summary = segment_summary(rows)
        self.assertEqual(sum(s["n"] for s in summary.values()), 100)

    def test_duplicate_fails(self):
        rows = demo_subscribers(5)
        with self.assertRaises(ValueError):
            segment_summary(rows + [rows[0]])


if __name__ == "__main__":
    unittest.main()
