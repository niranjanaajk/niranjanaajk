# Engineering Document Assistant

This offline prototype searches six synthetic engineering notes on topics including charging, telemetry ingestion, and manufacturing quality. TF-IDF ranks documents by lexical relevance. The assistant returns an exact source excerpt and citation, or marks queries below the relevance threshold for manual review.

```sh
python -m pip install -r requirements.txt
python assistant.py "connector handshake"
python assistant.py
```

The evaluation covers 12 supported queries and four empty or out-of-scope queries. It checks source identity, excerpt accuracy, and fallback. The cases are small and curated. This is a retrieval evaluation, with no live LLM or external engineering data.
