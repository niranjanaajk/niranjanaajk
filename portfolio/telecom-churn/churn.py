"""Telecom retention analysis with synthetic subscriber records.

Run: python churn.py
No external packages or downloads required.
"""
from collections import defaultdict
from random import Random


def demo_subscribers(n=1000, seed=2027):
    rng = Random(seed)
    customers = []
    for i in range(n):
        tenure = rng.randrange(1, 73)
        service_calls = rng.randrange(0, 7)
        contract = "monthly" if rng.random() < 0.55 else "annual"
        # Simulation only: this is not a trained predictive model.
        churn_prob = min(0.85, 0.06 + 0.07 * service_calls
                         + (0.11 if contract == "monthly" else 0)
                         + (0.09 if tenure < 6 else 0))
        customers.append({"customer_id": i, "tenure_months": tenure,
                          "service_calls": service_calls, "contract": contract,
                          "churned": int(rng.random() < churn_prob)})
    return customers


def segment_summary(customers):
    seen = set()
    segments = defaultdict(lambda: {"n": 0, "churned": 0})
    for customer in customers:
        identifier = customer["customer_id"]
        if identifier in seen:
            raise ValueError("Duplicate customer_id")
        seen.add(identifier)
        if customer["churned"] not in (0, 1):
            raise ValueError("Invalid churn label")
        segment = ("high-contact" if customer["service_calls"] >= 4 else "low-contact",
                   customer["contract"])
        segments[segment]["n"] += 1
        segments[segment]["churned"] += customer["churned"]
    return {key: {"n": value["n"],
                  "churn_rate": value["churned"] / value["n"]}
            for key, value in sorted(segments.items())}


if __name__ == "__main__":
    print("SYNTHETIC DEMO | Telecom churn by contact frequency and contract")
    for segment, stats in segment_summary(demo_subscribers()).items():
        print(f"{segment}: n={stats['n']}, churn_rate={stats['churn_rate']:.1%}")
    print("Observational segment differences are not causal effects.")
