# Telecom Customer Churn & Retention Segments

**Industry:** Telecommunications (T-Mobile)  
**Focus:** Customer data quality, retention segmentation, Python, interpretable metrics.

This runnable project creates synthetic subscriber records, checks uniqueness and churn labels, and measures churn across service-contact and contract segments. The results illustrate how a data scientist can **identify segments for further investigation**, not establish causality.

## Run
```bash
cd portfolio/telecom-churn
python churn.py
python -m unittest discover -s . -p 'test_*.py' -v
```

No external Python dependencies. All data is synthetic and deterministic. **No claims about T-Mobile customers or actual retention gains.**

## Next useful improvements
Add a train/test split, a regularized logistic-regression baseline, calibration, leakage checks, and an analysis of business costs.
