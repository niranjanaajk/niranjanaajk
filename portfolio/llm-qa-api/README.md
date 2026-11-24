# Contextual Q&A Service: Retrieval & API Reliability

**Industry:** Enterprise AI software / digital health (Amazon, Databricks, T-Mobile, KSU research)  
**Skills:** Python, information retrieval, dependency injection, application testing, fallback behavior.

This is a small runnable implementation of the **core logic** of an API-based contextual Q&A product. It retrieves text passages by lexical overlap, constructs a grounded prompt, and supports a supplied model callback. An offline deterministic model is used by default to avoid API costs and keep tests reproducible.

## Run
```bash
cd portfolio/llm-qa-api
python qa.py
python -m unittest discover -s . -p 'test_*.py' -v
```

There is **no web server or live LLM connected** in this iteration. The next milestone is adding a FastAPI REST endpoint, authenticated provider integration, retrieval evaluation, timeouts, and measured reliability tests. This project makes no medical advice claims.

## Knowledge Support Agent

Run `python support_agent.py "What should an outage report include?"`. The offline planner uses two read-only tools to search and open a sample document. Responses carry source IDs and an ordered tool trace, with manual review when evidence is missing. Tool calls are capped at three, and only previously retrieved documents can be opened. The planner is injectable. The default runs deterministically with no live model or API key.

Run `python -m unittest -v` for ten tests across the Q&A prototype and agent. The tests include nine supported questions with expected citations, three unmatched questions, and checks for invalid tool requests and the tool-call cap.
