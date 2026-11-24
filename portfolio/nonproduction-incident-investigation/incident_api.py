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


class IncidentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path)
        service = parse_qs(route.query).get("service", [""])[0].strip()
        if route.path != "/incidents":
            self.send_json(404, {"error": "Unknown endpoint"})
        elif not service:
            self.send_json(400, {"error": "service is required"})
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
