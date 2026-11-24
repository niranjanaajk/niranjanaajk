"""Predict energy intensity on held-out vehicles using synthetic trip telemetry."""
import json
import sqlite3
from contextlib import closing

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline


def make_trips():
    rng = np.random.default_rng(27)
    vehicle = np.repeat(np.arange(60), 40)
    n = len(vehicle)
    speed = rng.uniform(20, 120, n)
    temperature = rng.normal(18, 10, n)
    elevation = rng.uniform(0, 35, n)
    distance = rng.uniform(4, 150, n)
    energy_per_km = (
        135 + 0.010 * speed ** 2 + 0.9 * np.maximum(0, 18 - temperature)
        + 1.2 * elevation + rng.normal(0, 9, n) + rng.normal(0, 5, 60)[vehicle]
    )
    temperature[rng.choice(n, 110, replace=False)] = np.nan
    return pd.DataFrame({
        "vehicle_id": vehicle, "speed_kph": speed, "temperature_c": temperature,
        "distance_km": distance, "elevation_gain_m": distance * elevation,
        "energy_wh": energy_per_km * distance,
    })


def evaluate():
    with closing(sqlite3.connect(":memory:")) as db:
        make_trips().to_sql("trips", db, index=False)
        rows = pd.read_sql_query("""
            SELECT vehicle_id, speed_kph, temperature_c,
                   elevation_gain_m / distance_km AS climb_m_per_km,
                   energy_wh / distance_km AS target_wh_per_km
            FROM trips WHERE distance_km > 0
        """, db)
    y = rows.pop("target_wh_per_km")
    groups = rows.pop("vehicle_id")
    train, test = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=42)
                       .split(rows, y, groups))
    assert not set(groups.iloc[train]) & set(groups.iloc[test])
    models = {
        "median_baseline": DummyRegressor(strategy="median"),
        "random_forest": RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
    }
    errors = {}
    for name, estimator in models.items():
        model = make_pipeline(SimpleImputer(strategy="median"), estimator)
        model.fit(rows.iloc[train], y.iloc[train])
        errors[name] = round(mean_absolute_error(y.iloc[test], model.predict(rows.iloc[test])), 2)
    return {"synthetic_trips": len(rows), "vehicles": int(groups.nunique()),
            "holdout_vehicles": int(groups.iloc[test].nunique()), "holdout_trips": len(test),
            "mae_wh_per_km": errors}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
