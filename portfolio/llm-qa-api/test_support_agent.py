import unittest

from support_agent import run_agent


class AgentTests(unittest.TestCase):
    def test_supported_questions_and_citations(self):
        cases = {
            "password reset": "KB-01", "identity verification": "KB-01",
            "account portal": "KB-01", "billing dispute": "KB-02",
            "invoice number": "KB-02", "disputed amount": "KB-02",
            "outage report": "KB-03", "service symptoms": "KB-03",
            "symptoms started": "KB-03",
        }
        for question, ref in cases.items():
            with self.subTest(question=question):
                result = run_agent(question)
                self.assertEqual(result["citations"], [ref])
                self.assertIn(f"[{ref}]", result["answer"])
                self.assertFalse(result["manual_review"])

    def test_unmatched_questions(self):
        for question in ("photosynthesis", "chess opening", "volcano"):
            with self.subTest(question=question):
                self.assertTrue(run_agent(question)["manual_review"])

    def test_untrusted_reference(self):
        result = run_agent("password", lambda *_: {"tool": "read_document", "ref": "KB-01"})
        self.assertTrue(result["manual_review"])

    def test_unsupported_tool(self):
        result = run_agent("billing", lambda *_: {"tool": "delete_document"})
        self.assertTrue(result["manual_review"])

    def test_tool_budget(self):
        result = run_agent("outage", lambda *_: {"tool": "search_documents", "query": "outage"})
        self.assertEqual(len(result["trace"]), 3)

    def test_blank_question(self):
        with self.assertRaises(ValueError):
            run_agent(" ")
