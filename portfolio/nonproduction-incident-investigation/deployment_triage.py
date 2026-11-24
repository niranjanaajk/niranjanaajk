"""Offline, read-only deployment triage agent with an auditable tool trace."""
import argparse
import json
import sqlite3
from contextlib import closing

from incident_api import DATA, compare_windows
from runbook_assistant import recommend


def investigate_deployment(service, cutoff, incidents):
    """Invoke window comparison, evidence prioritization and runbook lookup."""
    changes = compare_windows(incidents, service, cutoff)
    regressions = [row for row in changes if row["delta"] > 0]
    if not changes:
        status = "insufficient_evidence"
    elif regressions:
        status = "investigate"
    else:
        status = "no_increase"

    with closing(sqlite3.connect(":memory:")) as db:
        checks = recommend(
            [{"signature": row["signature"], "count": row["current"]} for row in regressions],
            db,
        )
    return {
        "service": service,
        "baseline_minutes": [0, cutoff],
        "current_minutes": [cutoff, 2 * cutoff],
        "status": status,
        "changes": changes,
        "recommended_checks": checks,
        "tool_trace": [
            {"tool": "compare_windows", "signatures": len(changes)},
            {"tool": "prioritize_increases", "regressions": len(regressions)},
            {"tool": "lookup_runbooks", "citations": sum(bool(row["citation"]) for row in checks)},
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service")
    parser.add_argument("--cutoff", type=int, default=5)
    args = parser.parse_args()
    if not args.service.strip() or args.cutoff < 1:
        parser.error("Provide a nonblank service and a positive cutoff.")
    events = json.loads(DATA.read_text(encoding="utf-8"))
    print(json.dumps(investigate_deployment(args.service.strip(), args.cutoff, events), indent=2))


if __name__ == "__main__":
    main()
