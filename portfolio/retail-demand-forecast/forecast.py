"""Retail demand forecasting baseline, using only synthetic retail orders."""
from collections import defaultdict
from math import sqrt
from random import Random


def make_sales(days=210, seed=42):
    rng = Random(seed)
    records = []
    for day in range(days):
        for sku in ("essentials", "seasonal", "premium"):
            weekday = day % 7
            base = {"essentials": 65, "seasonal": 34, "premium": 19}[sku]
            weekend_effect = 12 if weekday in (5, 6) else 0
            trend = (day // 30) * (2 if sku == "essentials" else 0)
            sold = max(0, round(base + weekend_effect + trend + rng.gauss(0, 7)))
            records.append({"day": day, "sku": sku, "units": sold})
    return records


def seasonal_naive(records, holdout_days=28, season=7):
    if not records or holdout_days <= 0 or season <= 0:
        raise ValueError("Valid records, holdout_days, and season are required")
    by_sku = defaultdict(dict)
    for row in records:
        key = row["sku"]
        day = row["day"]
        if day in by_sku[key]:
            raise ValueError("Duplicate day/sku records")
        if row["units"] < 0:
            raise ValueError("Sales units cannot be negative")
        by_sku[key][day] = row["units"]
    last_day = max(r["day"] for r in records)
    cutoff = last_day + 1 - holdout_days
    details = []
    for sku, values in sorted(by_sku.items()):
        for day in sorted(values):
            if day < cutoff:
                continue
            ref_day = day - season
            # A non-leaky rolling baseline uses observed previous-week sales,
            # including observations available by this prediction time.
            if ref_day not in values:
                raise ValueError("Insufficient seasonal history")
            details.append({"sku": sku, "day": day, "actual": values[day],
                            "forecast": values[ref_day]})
    if not details:
        raise ValueError("No holdout records")
    errors = [r["forecast"] - r["actual"] for r in details]
    return {"n_predictions": len(errors),
            "mae": sum(abs(e) for e in errors) / len(errors),
            "rmse": sqrt(sum(e ** 2 for e in errors) / len(errors)),
            "wape": sum(abs(e) for e in errors) /
                    max(1, sum(r["actual"] for r in details))}


if __name__ == "__main__":
    result = seasonal_naive(make_sales())
    print("SYNTHETIC DEMO: daily retail demand, last 28 days")
    for key, value in result.items():
        print(f"{key}: {value:.3f}" if isinstance(value, float)
              else f"{key}: {value}")
