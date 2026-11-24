import json
import sqlite3
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from agent import run_agent
from incident_api import IncidentHandler
from runbook_assistant import recommend


class PortfolioTests(unittest.TestCase):
    def test_rest_recurrence_and_invalid_request(self):
        with ThreadingHTTPServer(("127.0.0.1", 0), IncidentHandler) as server:
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/incidents"
                with urlopen(url + "?service=checkout", timeout=2) as response:
                    rows = json.load(response)["failures"]
                self.assertEqual(rows[0], {"signature": "DB_POOL_TIMEOUT", "count": 2})
                with self.assertRaises(HTTPError) as error:
                    urlopen(url, timeout=2)
                self.assertEqual(error.exception.code, 400)
                error.exception.close()
            finally:
                server.shutdown()
                thread.join()

    def test_sqlite_citation_and_missing_runbook(self):
        rows = [{"signature": "DB_POOL_TIMEOUT", "count": 2}, {"signature": "UNKNOWN", "count": 1}]
        with sqlite3.connect(":memory:") as database:
            self.assertEqual([item["citation"] for item in recommend(rows, database)], ["RB-01", None])

    def test_agent_uses_tool_and_falls_back_when_citation_missing(self):
        evidence = [{"signature": "DB_POOL_TIMEOUT", "count": 2, "citation": "RB-01"}]

        def complete(messages, tools):
            if tools:
                return {"tool_calls": [{
                    "id": "call_1", "type": "function",
                    "function": {"name": "investigate_service", "arguments": '{"service":"checkout"}'},
                }]}
            self.assertEqual(json.loads(messages[-1]["content"]), evidence)
            return {"content": "Check the pool."}

        def investigate(service):
            self.assertEqual(service, "checkout")
            return evidence

        result = run_agent("Why is checkout failing?", complete, investigate)
        self.assertEqual(result["evidence"], evidence)
        self.assertTrue(result["answer"].startswith("Review the incident counts"))


if __name__ == "__main__":
    unittest.main()
