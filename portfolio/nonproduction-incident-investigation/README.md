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
