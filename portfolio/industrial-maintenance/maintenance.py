"""Industrial equipment failure-risk baseline with synthetic telemetry.

Runs on Python standard library only:
    python maintenance.py

This is a reproducible portfolio demonstration, NOT a Caterpillar system.
"""
from math import exp, log
from random import Random


def make_telemetry(n=1200, seed=2027):
    """Simulate machine sensor snapshots with labeled 30-day failure windows."""
    if n < 100:
        raise ValueError("n must be at least 100")
    rng = Random(seed)
    readings = []
    for i in range(n):
        temperature_c = rng.uniform(55, 110)
        vibration_mm_s = rng.uniform(1, 10)
        operating_hours = rng.randrange(100, 15000)
        pressure_bar = rng.uniform(2.0, 8.0)
        # Synthetic process used only to generate demonstrative labels.
        z = (-5.0 + 0.045 * (temperature_c - 70)
             + 0.38 * (vibration_mm_s - 4)
             + 0.00010 * operating_hours
             + 0.20 * max(0, 4 - pressure_bar))
        failure = int(rng.random() < 1 / (1 + exp(-z)))
        readings.append({
            "snapshot_id": i, "temperature_c": round(temperature_c, 3),
            "vibration_mm_s": round(vibration_mm_s, 3),
            "operating_hours": operating_hours, "pressure_bar": round(pressure_bar, 3),
            "failure_30d": failure
        })
    return readings


def features(row):
    """Normalize sensor inputs without fitting to the holdout data."""
    return [(row["temperature_c"] - 70) / 30,
            (row["vibration_mm_s"] - 4) / 5,
            row["operating_hours"] / 15000,
            (row["pressure_bar"] - 5) / 3]


def sigmoid(value):
    return 1 / (1 + exp(-max(-30, min(30, value))))


def train_logistic(rows, steps=600, learning_rate=0.2):
    """Fit a small regularized logistic classifier using batch gradient descent."""
    if not rows or steps < 1:
        raise ValueError("Training rows and iterations are required")
    n = len(rows)
    weights = [0.0] * 5
    for _ in range(steps):
        gradient = [0.0] * 5
        for row in rows:
            x = [1.0] + features(row)
            residual = sigmoid(sum(w * a for w, a in zip(weights, x))) - row["failure_30d"]
            for j in range(5):
                gradient[j] += residual * x[j]
        for j in range(5):
            penalty = 0.02 * weights[j] if j else 0.0
            weights[j] -= learning_rate * (gradient[j] / n + penalty)
    return weights


def probabilities(rows, weights):
    return [sigmoid(sum(w * x for w, x in zip(weights, [1.0] + features(r))))
            for r in rows]


def evaluate(rows, scores, threshold=0.25):
    if len(rows) != len(scores) or not rows:
        raise ValueError("Labels and probability scores must align")
    tp = fp = tn = fn = 0
    for row, score in zip(rows, scores):
        if not 0 <= score <= 1:
            raise ValueError("Scores must be probabilities")
        actual = row["failure_30d"]
        if actual not in (0, 1):
            raise ValueError("Invalid failure label")
        predicted = int(score >= threshold)
        if predicted and actual:
            tp += 1
        elif predicted:
            fp += 1
        elif actual:
            fn += 1
        else:
            tn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "alert_rate": (tp + fp) / len(rows), "tp": tp, "fp": fp, "tn": tn, "fn": fn}


def main():
    data = make_telemetry()
    # Chronological simulation split by snapshot ID: later records are held out.
    split_at = int(len(data) * 0.8)
    train, test = data[:split_at], data[split_at:]
    fitted = train_logistic(train)
    test_scores = probabilities(test, fitted)
    report = evaluate(test, test_scores)
    print("SYNTHETIC TELEMETRY | Equipment Failure Risk (30-day horizon)")
    print(f"Training snapshots: {len(train)} | Holdout snapshots: {len(test)}")
    for key, value in report.items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")
    print("Metrics are synthetic demo measurements, not real-world equipment reliability.")


if __name__ == "__main__":
    main()
