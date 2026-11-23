"""Reproducible product A/B experiment analysis using standard-library Python.

All demo data is synthetic. Nothing here represents actual users.
Run: python experiment.py
"""
from collections import defaultdict
from math import sqrt
from random import Random


def demo_events(seed=17, n=2000):
    rng = Random(seed)
    events = []
    for i in range(n):
        group = "control" if i % 2 == 0 else "treatment"
        # Synthetic simulated lift, not a claim about a real product.
        probability = 0.12 if group == "control" else 0.15
        events.append({"user_id": i, "variant": group,
                       "converted": int(rng.random() < probability)})
    return events


def analyze(events):
    groups = defaultdict(list)
    ids = set()
    for row in events:
        user = row["user_id"]
        if user in ids:
            raise ValueError("Duplicate user_id; deduplicate before analysis")
        ids.add(user)
        if row["variant"] not in ("control", "treatment"):
            raise ValueError("Unexpected experiment variant")
        if row["converted"] not in (0, 1):
            raise ValueError("Conversion must be binary")
        groups[row["variant"]].append(row["converted"])

    if not groups["control"] or not groups["treatment"]:
        raise ValueError("Both experiment groups are required")
    nc, nt = len(groups["control"]), len(groups["treatment"])
    pc = sum(groups["control"]) / nc
    pt = sum(groups["treatment"]) / nt
    difference = pt - pc
    standard_error = sqrt(pc * (1 - pc) / nc + pt * (1 - pt) / nt)
    return {"control_n": nc, "treatment_n": nt,
            "control_conversion": pc, "treatment_conversion": pt,
            "absolute_lift": difference,
            "ci_95_lower": difference - 1.96 * standard_error,
            "ci_95_upper": difference + 1.96 * standard_error}


if __name__ == "__main__":
    summary = analyze(demo_events())
    print("SYNTHETIC DEMO | Experiment impact on conversion")
    for name, value in summary.items():
        print(f"{name}: {value:.4f}" if isinstance(value, float)
              else f"{name}: {value}")
    print("Confidence interval is descriptive; check randomization and power before decisions.")
