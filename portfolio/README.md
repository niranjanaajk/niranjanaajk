# Industry-Focused AI, Data Science & Software Engineering Portfolio

This repository contains **seven runnable mini-projects** across real business problem domains. Every demo uses **synthetic data or a small local knowledge base**, avoiding private information or unsupported performance claims. The code is developed as portfolio work, not on behalf of any listed company.

| Project | Industry | Technical focus |
| --- | --- | --- |
| [Product experimentation](product-experimentation/) | SaaS / cloud | A/B testing, conversion lift, confidence intervals, validation |
| [Telecom churn](telecom-churn/) | Telecommunications | Retention cohorts, segmentation, Python |
| [Industrial predictive maintenance](industrial-maintenance/) | Industrial machinery | Sensor telemetry, logistic regression, holdout validation, F1 |
| [Retail demand forecast](retail-demand-forecast/) | Retail / operations | Time-series baselines, MAE, RMSE, WAPE |
| [Transaction risk triage](fintech-transaction-risk/) | Financial services | Risk screening, precision/recall, explainability |
| [Healthcare readmissions](healthcare-readmission/) | Digital health | Cohort analysis, 30-day outcomes, safe data handling |
| [Contextual Q&A service](llm-qa-api/) | AI software | Retrieval, dependency injection, fallback logic, unit testing |

## Run all project checks

Each project is deliberately standard-library-only, so the code is easy to run:

```bash
python -m unittest discover -s portfolio/product-experimentation -p 'test_*.py' -v
python -m unittest discover -s portfolio/telecom-churn -p 'test_*.py' -v
python -m unittest discover -s portfolio/industrial-maintenance -p 'test_*.py' -v
python -m unittest discover -s portfolio/retail-demand-forecast -p 'test_*.py' -v
python -m unittest discover -s portfolio/fintech-transaction-risk -p 'test_*.py' -v
python -m unittest discover -s portfolio/healthcare-readmission -p 'test_*.py' -v
python -m unittest discover -s portfolio/llm-qa-api -p 'test_*.py' -v
```

All project test modules are included. GitHub Actions is intended to run them on pull requests, pushes, and scheduled maintenance checks. **Automatic test runs are not automatic proof of new code contributions.**

## Portfolio principles

- Reproducible analysis and clear input validation
- Honest separation of synthetic/demo metrics from operational results
- Interview-ready code that can be expanded with real permitted datasets
- No claim of affiliation with the employers whose industries inspired project topics

## Recommended future upgrades

Move the strongest projects into dedicated repositories after adding dataset documentation, notebooks, richer model comparisons, and deployed demos. Especially valuable: model calibration and PR-AUC for industrial risk, uplift and sample-size planning for experimentation, and a FastAPI service for contextual Q&A.
