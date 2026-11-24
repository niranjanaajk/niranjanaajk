"""Check expected decisions, regression counts and citations on synthetic cases."""
import json
from itertools import product

from deployment_triage import investigate_deployment


def main():
    executed = 0
    matched = 0
    for (signature, citation), before, after in product(
        [("DB_POOL_TIMEOUT", "RB-01"), ("CACHE_MISS", "RB-02"), ("UNKNOWN", None)],
        range(4),
        range(4),
    ):
        events = [
            {"service": "target", "signature": signature, "minute": minute}
            for minute, count in [(0, before), (5, after)]
            for _ in range(count)
        ]
        events.extend([
            {"service": "other", "signature": signature, "minute": 5},
            {"service": "target", "signature": signature, "minute": 10},
        ])
        result = investigate_deployment("target", 5, events)
        expected_status = (
            "investigate" if after > before else
            "no_increase" if before or after else "insufficient_evidence"
        )
        expected_checks = (
            [{"signature": signature, "count": after, "citation": citation}]
            if after > before else []
        )
        observed_checks = [
            {key: row[key] for key in ("signature", "count", "citation")}
            for row in result["recommended_checks"]
        ]
        executed += 1
        if result["status"] == expected_status and observed_checks == expected_checks:
            matched += 1
        else:
            print(json.dumps({"failed_case": [signature, before, after], "result": result}))
    print(json.dumps({"matched": matched, "synthetic_cases": executed}, indent=2))
    return 0 if matched == executed else 1


if __name__ == "__main__":
    raise SystemExit(main())
