"""Test the real loopback HTTP and SQLite path with a simulated model provider."""
import json
import unittest
from functools import partial

from agent import investigate, run_agent
from reliability_drill import running_api


def simulate_model(service, reply):
    def complete(messages, tools):
        if tools:
            return {"tool_calls": [{"id": "local-test", "function": {
                "name": "investigate_service",
                "arguments": json.dumps({"service": service}),
            }}]}
        if reply is None:
            raise TimeoutError("Simulated provider timeout")
        return {"content": reply}
    return complete


class RunbookIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server = running_api()
        cls.port = server.__enter__()
        cls.addClassCleanup(server.__exit__, None, None, None)

    def run_investigation(self, service, reply):
        return run_agent(f"Investigate {service}", simulate_model(service, reply),
                         partial(investigate, port=self.port))

    def test_evidence_and_citations_flow_through_http_and_sqlite(self):
        result = self.run_investigation("checkout", "Review RB-01 and RB-02.")
        self.assertEqual(result["summary_source"], "model")
        self.assertEqual(
            [(row["count"], row["citation"]) for row in result["evidence"]],
            [(2, "RB-01"), (1, "RB-02")],
        )

    def test_provider_timeout_preserves_cited_evidence(self):
        result = self.run_investigation("checkout", None)
        self.assertEqual(result["summary_source"], "evidence")
        self.assertIn("DB_POOL_TIMEOUT: 2 events", result["answer"])
        self.assertIn("[RB-01]", result["answer"])

    def test_unknown_service_returns_no_evidence(self):
        result = self.run_investigation("unknown", None)
        self.assertEqual(result["evidence"], [])
        self.assertIn("No incident evidence", result["answer"])
