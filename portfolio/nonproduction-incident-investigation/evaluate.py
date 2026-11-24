"""Repeatable offline acceptance checks. Run with python evaluate.py."""
import json
import sqlite3
from urllib.error import URLError

from agent import run_agent
from incident_api import DATA, compare_windows, summarize
from runbook_assistant import recommend


def check_agent(rows, model_summary):
    def complete(messages, tools):
        if tools:
            return {"tool_calls": [{"id": "example", "function": {
                "name": "investigate_service", "arguments": '{"service":"checkout"}'
            }}]}
        if model_summary is None:
            raise URLError("simulated timeout")
        return {"content": model_summary}

    return run_agent("Investigate checkout", complete, lambda service: rows)


def main():
    events = json.loads(DATA.read_text(encoding="utf-8"))
    with sqlite3.connect(":memory:") as conn:
        evidence = recommend(summarize(events, "checkout"), conn)
        unknown = recommend([{"signature": "UNKNOWN", "count": 1}], conn)[0]
    cases = {
        "recurring_failure_rank": evidence[0]["signature"] == "DB_POOL_TIMEOUT" and evidence[0]["count"] == 2,
        "window_delta": [(r["signature"], r["delta"]) for r in compare_windows(events, "checkout", 5)]
            == [("CACHE_MISS", 1), ("DB_POOL_TIMEOUT", 0)],
        "no_events": summarize(events, "unknown") == [],
        "unknown_runbook": unknown["citation"] is None,
        "known_citations": check_agent(evidence, "See RB-01 and RB-02.")["summary_source"] == "model",
        "missing_citation": check_agent(evidence, "See RB-01.")["summary_source"] == "evidence",
        "invented_citation": check_agent(evidence, "See RB-01, RB-02 and RB-99.")["summary_source"] == "evidence",
        "provider_timeout": check_agent(evidence, None)["summary_source"] == "evidence",
    }
    print(json.dumps({"passed": sum(cases.values()), "total": len(cases), "cases": cases}, indent=2))
    return 0 if all(cases.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
