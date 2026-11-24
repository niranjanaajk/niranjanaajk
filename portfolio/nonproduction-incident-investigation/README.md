# Nonproduction Incident Investigation

Two connected portfolio projects demonstrate failure analysis and AI-assisted investigation using synthetic engineering data.

## 1. Incident Trends API

Run `python incident_api.py` and open http://127.0.0.1:8080/incidents?service=checkout. The read-only REST API groups incident signatures by service, ranks recurring failures, and returns JSON evidence. The checkout fixture contains two database pool timeouts and one cache miss.

## 2. Runbook Investigation Agent

In another terminal, run `python runbook_assistant.py checkout` for deterministic retrieval. It calls the incident API, looks up matching runbooks in SQLite, and returns incident counts, source IDs, and suggested checks. Unmatched signatures are flagged for manual review.

For model-driven tool calling, set `OPENAI_API_KEY` in your environment and run `python agent.py "What is recurring in checkout and what should I investigate?"`. The agent lets the model select a service, executes one allowlisted read-only tool, and asks the model to summarize the returned evidence. The structured evidence is always retained. Missing citations trigger a fallback. Incident frequency and runbook guidance inform investigation but do not establish root cause.

## Verification

Run `python -m unittest -v` (Python 3.10+). The local tests cover the REST endpoint, recurrence counts, invalid requests, SQLite provenance, missing runbooks, and the model tool-call path with a stubbed provider. Live LLM output requires a provider key and has not been verified. The sample contains no production records, customer data, or credentials.

## Compare an incident window against its baseline

With the API running, open http://127.0.0.1:8080/comparison?service=checkout&cutoff=5. The endpoint compares minutes 0–4 with 5–9 and ranks changes by count difference. A case at the exact cutoff belongs to the current window. For checkout, cache misses increase by one and pool timeout counts are flat across the two windows.

## Offline acceptance evaluation

Run `python evaluate.py` to check eight deterministic scenarios, including window boundaries, missing runbooks, invented citations, and simulated model timeouts. The CLI exits with a nonzero status on failure. The agent checks citation IDs against retrieved evidence and renders deterministic findings when the summary cannot be checked. Citation matching does not establish that every sentence in a model summary is factually supported.

## In progress: Deployment Triage Agent

Run `python deployment_triage.py checkout --cutoff 5`. This offline agent runs three read-only steps: compare failure counts across two equal windows, prioritize increases, and look up SQLite runbooks. The response includes an ordered tool trace and citations. Missing runbooks are flagged for manual review. A count increase is a signal to investigate, not evidence that a deployment caused it.

Run `python evaluate_deployment.py` to evaluate 48 synthetic cases (three signatures and four possible counts in each window). Each case checks the expected triage status and any recommended checks or citation IDs. The benchmark covers unrelated-service events and the exclusive upper window boundary. It measures this deterministic workflow only. Live model evaluation and real deployment telemetry are outside this version.

## Local reliability drill

Run `python reliability_drill.py` to exercise baseline availability, a controlled local shutdown, and recovery after restarting the API on the same port. The probe checks the response payload and records elapsed time in milliseconds. The command exits with a failure status unless all three phases match the expected healthy, unavailable, and recovered states. Use the JSON output to document the incident timeline. Probe timings vary by machine. This loopback drill exercises a simulated outage against synthetic incident data.

## Agent integration tests

Run `python -m unittest -v` to test tool orchestration through the local REST server and SQLite. The three integration tests cover cited evidence, deterministic fallback after a simulated provider timeout, and a service with no incident data. The model provider is simulated, while the HTTP and SQLite calls run locally.
