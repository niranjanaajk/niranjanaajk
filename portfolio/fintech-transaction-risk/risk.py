"""Transparent transaction-risk triage using synthetic payment events."""
from collections import Counter
from random import Random


def make_transactions(n=1500, seed=31):
    rng = Random(seed)
    records = []
    for i in range(n):
        amount = round(rng.expovariate(1 / 85) + 1, 2)
        international = int(rng.random() < 0.14)
        new_device = int(rng.random() < 0.18)
        velocity = rng.randrange(1, 9)
        # Synthetic label generation for illustration only.
        risk_probability = min(0.8, 0.015 + 0.09 * international
                               + 0.08 * new_device + 0.025 * (velocity > 5)
                               + 0.07 * (amount > 300))
        records.append({"transaction_id": i, "amount_usd": amount,
                        "international": international, "new_device": new_device,
                        "hourly_velocity": velocity,
                        "flagged_fraud": int(rng.random() < risk_probability)})
    return records


def risk_score(txn):
    """Explainable heuristic triage score, not a trained fraud model."""
    return min(1.0, 0.01 + 0.30 * txn["international"]
               + 0.28 * txn["new_device"]
               + 0.22 * (txn["hourly_velocity"] > 5)
               + 0.15 * (txn["amount_usd"] > 300))


def evaluate_triage(transactions, threshold=0.4):
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must lie between 0 and 1")
    seen = set()
    counts = Counter()
    for transaction in transactions:
        identifier = transaction["transaction_id"]
        if identifier in seen:
            raise ValueError("Duplicate transaction_id")
        seen.add(identifier)
        actual = transaction["flagged_fraud"]
        if actual not in (0, 1):
            raise ValueError("Invalid target")
        predicted = int(risk_score(transaction) >= threshold)
        if predicted and actual:
            counts["tp"] += 1
        elif predicted:
            counts["fp"] += 1
        elif actual:
            counts["fn"] += 1
        else:
            counts["tn"] += 1
    if not transactions:
        raise ValueError("At least one transaction is required")
    precision = counts["tp"] / max(1, counts["tp"] + counts["fp"])
    recall = counts["tp"] / max(1, counts["tp"] + counts["fn"])
    return {"transactions": len(transactions), "alerts": counts["tp"] + counts["fp"],
            "precision": precision, "recall": recall,
            "false_positives": counts["fp"]}


if __name__ == "__main__":
    report = evaluate_triage(make_transactions())
    print("SYNTHETIC DEMO: transaction risk alert triage")
    for key, value in report.items():
        print(f"{key}: {value:.3f}" if isinstance(value, float)
              else f"{key}: {value}")
