import unittest
from experiment import analyze, demo_events


class ExperimentTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(demo_events(), demo_events())

    def test_valid_output(self):
        result = analyze(demo_events(n=400))
        self.assertEqual(result["control_n"], 200)
        self.assertEqual(result["treatment_n"], 200)
        self.assertLessEqual(result["ci_95_lower"], result["ci_95_upper"])

    def test_duplicates_rejected(self):
        rows = demo_events(n=10)
        with self.assertRaises(ValueError):
            analyze(rows + [rows[0]])

    def test_missing_group_rejected(self):
        with self.assertRaises(ValueError):
            analyze([{"user_id": 1, "variant": "control", "converted": 1}])


if __name__ == "__main__":
    unittest.main()
