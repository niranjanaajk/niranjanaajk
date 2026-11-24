"""Exercise local availability monitoring and recovery against the incident API."""
import contextlib
import json
from http.server import ThreadingHTTPServer
import threading
from time import perf_counter
from urllib.error import URLError
from urllib.request import urlopen

from incident_api import IncidentHandler


@contextlib.contextmanager
def running_api(port=0):
    with ThreadingHTTPServer(("127.0.0.1", port), IncidentHandler) as server:
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        try:
            yield server.server_port
        finally:
            server.shutdown()
            worker.join()


def probe(port):
    start = perf_counter()
    try:
        with urlopen(f"http://127.0.0.1:{port}/incidents?service=checkout", timeout=1) as response:
            body = json.load(response)
        healthy = body.get("service") == "checkout" and isinstance(body.get("failures"), list)
    except (URLError, OSError, ValueError, AttributeError):
        healthy = False
    return {"healthy": healthy, "probe_ms": round((perf_counter() - start) * 1000, 2)}


def main():
    with running_api() as port:
        before = probe(port)
    during = probe(port)
    with running_api(port):
        after = probe(port)
    phases = {"baseline": before, "simulated_outage": during, "recovered": after}
    expected = {"baseline": True, "simulated_outage": False, "recovered": True}
    matches = sum(phases[name]["healthy"] == state for name, state in expected.items())
    print(json.dumps({"expected_transitions_matched": matches, "phases": phases}, indent=2))
    return 0 if matches == len(expected) else 1


if __name__ == "__main__":
    raise SystemExit(main())
