"""Use incident counts to retrieve evidence from synthetic runbooks in SQLite."""
import argparse
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

RUNBOOKS = {
    "DB_POOL_TIMEOUT": ("RB-01", "Inspect pool utilization and recent connection-setting changes."),
    "CACHE_MISS": ("RB-02", "Compare cache hit rate against recent deploys and cache warm-up."),
}


def recommend(failures, database):
    database.execute("CREATE TABLE IF NOT EXISTS runbooks (signature TEXT PRIMARY KEY, citation TEXT, guidance TEXT)")
    database.executemany(
        "INSERT OR REPLACE INTO runbooks VALUES (?, ?, ?)",
        [(signature, *runbook) for signature, runbook in RUNBOOKS.items()],
    )
    results = []
    for failure in failures:
        match = database.execute(
            "SELECT citation, guidance FROM runbooks WHERE signature = ?",
            (failure["signature"],),
        ).fetchone()
        results.append({
            **failure,
            "citation": match[0] if match else None,
            "next_check": match[1] if match else "No matching runbook. Escalate for manual review.",
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service")
    parser.add_argument("--database", type=Path, default=Path("runbooks.sqlite3"))
    args = parser.parse_args()
    query = urlencode({"service": args.service})
    with urlopen("http://127.0.0.1:8080/incidents?" + query, timeout=5) as response:
        incidents = json.load(response)
    with sqlite3.connect(args.database) as database:
        print(json.dumps(recommend(incidents["failures"], database), indent=2))


if __name__ == "__main__":
    main()
