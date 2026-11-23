import unittest
from qa import answer_question, retrieve


class QATests(unittest.TestCase):
    def setUp(self):
        self.docs = ["An API returns structured JSON responses.",
                     "The service logs errors and retry outcomes."]

    def test_retrieval(self):
        self.assertIn(self.docs[0], retrieve("API JSON", self.docs))

    def test_fallback(self):
        result = answer_question("quantum physics", self.docs)
        self.assertTrue(result.fallback)
        self.assertFalse(result.evidence)

    def test_injectable_client(self):
        result = answer_question("API JSON", self.docs, model=lambda prompt: "A tested response.")
        self.assertEqual(result.text, "A tested response.")

    def test_empty_question(self):
        with self.assertRaises(ValueError):
            answer_question("  ", self.docs)


if __name__ == "__main__":
    unittest.main()
