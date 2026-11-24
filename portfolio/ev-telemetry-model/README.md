# EV Telemetry Energy Intensity Model

Predict trip energy intensity in watt-hours per kilometer using synthetic telemetry. The script generates 2,400 trips across 60 vehicles, derives features in SQL, and uses training-only median imputation for 110 missing temperature readings. A grouped holdout keeps all trips from each vehicle on one side of the split.

Run with Python 3.11 or newer:

```sh
python -m pip install -r requirements.txt
python run.py
```

The script compares mean absolute error for a median baseline and a random forest. See results.json for the measured holdout. This synthetic data is generated from a known energy equation and provides no evidence of performance on real vehicles.
