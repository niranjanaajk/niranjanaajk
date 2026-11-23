import unittest
from readmission import cohort_readmission_rates, make_encounters


class ReadmissionTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(make_encounters(100), make_encounters(100))

    def test_cohort_counts(self):
        result = cohort_readmission_rates(make_encounters(300))
        self.assertEqual(sum(x["encounters"] for x in result.values()), 300)

    def test_duplicate(self):
        records = make_encounters(20)
        with self.assertRaises(ValueError):
            cohort_readmission_rates(records + [records[0]])

    def test_empty(self):
        with self.assertRaises(ValueError):
            cohort_readmission_rates([])


if __name__ == "__main__":
    unittest.main()
