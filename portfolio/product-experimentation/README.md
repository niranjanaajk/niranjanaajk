# Product Experimentation & Conversion Analysis

**Industry:** SaaS / product analytics (Databricks, Amazon)  
**Focus:** Experiment design, conversion measurement, Python, uncertainty, data validation.

This runnable mini-project simulates a randomized A/B experiment and reports treatment/control conversion rates, absolute lift, and a 95% confidence interval. It rejects duplicate users and malformed assignments. **All examples are synthetic; no actual business impact is claimed.**

## Run
```bash
cd portfolio/product-experimentation
python experiment.py
python -m unittest discover -s . -p 'test_*.py' -v
```

## Analytical limitations
- The normal-approximation CI is less reliable for rare events and small sample sizes.
- This demo does not model sample-ratio mismatch, sequential testing, power, spillovers, or multiple comparisons.
- A production analysis would include pre-registered metrics, guardrails, and segment/cohort checks.

## Next useful improvements
Add event ingestion from CSV/SQL, sample-ratio checks, and a notebook comparing frequentist and bootstrap intervals.
