"""Read-only REST API over synthetic nonproduction incidents."""
import json
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

DATA = Path(__file__).with_name("incidents.json")


def summarize(incidents, service):
    counts = Counter(row["signature"] for row in incidents if row["service"] == service)
    return [
        {"signature": signature, "count": count}
        for signature, count in sorted(counts.items(), key=lambda row: (-row[1], row[0]))
    ]


def compare_windows(incidents, service, cutoff):
    """Compare equal-length windows on either side of a minute boundary."""
    before = Counter()
    after = Counter()
    for row in incidents:
        if row["service"] != service:
            continue
        minute = row["minute"]
        if 0 <= minute < cutoff:
            before[row["signature"]] += 1
        elif cutoff <= minute < 2 * cutoff:
            after[row["signature"]] += 1
    changes = [
        {"signature": signature, "baseline": before[signature],
         "current": after[signature], "delta": after[signature] - before[signature]}
        for signature in before.keys() | after.keys()
    ]
    return sorted(changes, key=lambda row: (-row["delta"], row["signature"]))


class IncidentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path)
        params = parse_qs(route.query)
        service = params.get("service", [""])[0].strip()
        if route.path not in {"/incidents", "/comparison"}:
            self.send_json(404, {"error": "Unknown endpoint"})
        elif not service:
            self.send_json(400, {"error": "service is required"})
        elif route.path == "/comparison":
            raw_cutoff = params.get("cutoff", [""])[0]
            if not raw_cutoff.isascii() or not raw_cutoff.isdecimal() or len(raw_cutoff) > 4 or int(raw_cutoff) == 0:
                self.send_json(400, {"error": "cutoff must be an integer between 1 and 9999"})
                return
            incidents = json.loads(DATA.read_text(encoding="utf-8"))
            cutoff = int(raw_cutoff)
            self.send_json(200, {"service": service, "cutoff": cutoff,
                                 "changes": compare_windows(incidents, service, cutoff)})
        else:
            incidents = json.loads(DATA.read_text(encoding="utf-8"))
            self.send_json(200, {"service": service, "failures": summarize(incidents, service)})

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", 8080), IncidentHandler) as server:
        server.serve_forever()
