# Industrial Equipment Predictive Maintenance & Failure Risk

**Industry:** Industrial machinery and heavy equipment (relevant to Caterpillar)  
**Skills:** Python, synthetic telematics, predictive classification, feature engineering, time-ordered holdout, evaluation, automated tests.

## Problem
Equipment failures can interrupt operations and increase maintenance costs. This portfolio example models the problem of identifying **equipment snapshots at elevated risk of failure within the following 30 days**, to support prioritizing inspection candidates.

## What the implementation actually does
1. Generates reproducible **synthetic** machine readings: temperature, vibration, operating hours, pressure and simulated failure labels.
2. Engineers normalized numeric features and fits a regularized **logistic regression classifier implemented in pure Python**.
3. Holds out the latest 20% of simulated snapshots for evaluation, rather than shuffling future records into training.
4. Reports **precision, recall, F1, alert rate, and confusion-matrix counts** at a stated decision threshold.
5. Uses unit tests for data reproducibility, model output, evaluation bounds, and invalid inputs.

## Run
```bash
cd portfolio/industrial-maintenance
python maintenance.py
python -m unittest discover -s . -p 'test_*.py' -v
```

Requires Python 3.9+ and no external packages.

## Important limitations
**Synthetic data only; no Caterpillar affiliation, internal datasets, operational savings, or real machine-failure performance is claimed.** Snapshots are illustrative and not a real longitudinal fleet dataset. The labels come from a known simulated data-generating process; production use would require real asset/time identifiers, no-leakage labeling, equipment-class segmentation, probability calibration, failure-cost estimates, human review, and monitoring for distribution shift.

## Suggested next iteration
Add a machine-level temporal split, sensor drift detection, PR-AUC and calibration metrics, and a small FastAPI endpoint for risk scoring.
