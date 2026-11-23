# Healthcare Readmission Cohort Analysis

**Industry:** Healthcare / digital health (Emory, healthcare AI research)  
**Skills:** Python, cohort analysis, outcome definition, data-quality checks, ethical communication.

## Overview
This portfolio project analyzes a **synthetic** set of hospital encounters for 30-day readmission patterns. It compares higher and lower prior-utilization cohorts and provides repeatable quality controls. The cohort output is descriptive, not causal, and does not make individual clinical predictions.

## Run
```bash
cd portfolio/healthcare-readmission
python readmission.py
python -m unittest discover -s . -p 'test_*.py' -v
```

No external dependencies or patient-identifying information.

## Responsible-use note
This is a demonstrative learning project, not a medical device, clinical recommendation, or validated predictive model. Real healthcare work requires privacy protections, validation by clinicians, fairness analyses and independent external evaluation.

## Next steps
Confidence intervals for readmission rates, a defined cohort eligibility window, time-aware validation, and documentation of clinical stakeholders' requirements.
