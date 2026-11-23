# Retail Demand Forecasting & Inventory Planning

**Industry:** Retail / supply chain (Home Depot, Lowe's, Amazon)  
**Skills:** Python, time-series validation, seasonal forecasting, MAE, RMSE, WAPE, data integrity.

## Overview
Forecast daily item demand to inform replenishment decisions. The example generates reproducible **synthetic** sales records for three SKUs and evaluates a 7-day seasonal-naive forecast on a 28-day holdout. A transparent baseline is a useful first step before trying boosted trees or deep learning.

## Run
```bash
cd portfolio/retail-demand-forecast
python forecast.py
python -m unittest discover -s . -p 'test_*.py' -v
```

No external dependencies. All reported performance is on synthetic data, not a real retailer.

## Next steps
Add promotions and holidays, a realistic lead-time inventory policy, rolling-origin backtesting, and a comparison to gradient-boosted models. Avoid using future sales to create current forecasts.
