# Explainable Transaction Risk & Alert Prioritization

**Industry:** Financial services / payment systems (Visa, Capital One, Truist, Equifax, ICE)  
**Skills:** Python, anomaly/risk triage, imbalanced outcomes, precision/recall, data validation.

## Overview
This small example synthesizes transactions with amount, device, geography, and velocity features. A transparent, hand-designed scoring function prioritizes higher-risk transactions for review. Tests enforce transaction uniqueness and sensible score bounds. Precision, recall and false-positive counts make alert trade-offs visible.

## Run
```bash
cd portfolio/fintech-transaction-risk
python risk.py
python -m unittest discover -s . -p 'test_*.py' -v
```

## Scope and limitations
All transactions and labels are **synthetic**. This is **not** a trained fraud detector, regulatory assessment, or a recommendation to decline financial transactions. No real bank or card-network data is used.

## Next steps
Train a calibrated classifier on appropriately permissioned data; evaluate precision-recall curves, model drift, fairness, explainability and human-review costs.
