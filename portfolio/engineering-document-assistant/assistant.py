"""Offline evidence-first search over a small synthetic engineering corpus."""
import argparse
import json

from sklearn.feature_extraction.text import TfidfVectorizer

DOCS = {
    "BAT-01": "Battery pack temperature excursions require reviewing coolant flow and sensor calibration.",
    "CHG-01": "Charging session failures require checking connector status and handshake events.",
    "TEL-01": "Missing telemetry packets require checking ingestion timestamps and queue backlogs.",
    "MFG-01": "Assembly torque deviations require reviewing station measurements and tool calibration.",
    "QLT-01": "Quality inspection defects should be logged with batch identifier and inspection station.",
    "REL-01": "Deployment rollback requires confirming service health and recording the release version.",
}

CASES = [
    ("battery pack temperature", "BAT-01"), ("coolant flow", "BAT-01"),
    ("charging session fails", "CHG-01"), ("connector handshake", "CHG-01"),
    ("missing telemetry", "TEL-01"), ("ingestion timestamps", "TEL-01"),
    ("assembly torque", "MFG-01"), ("station measurements", "MFG-01"),
    ("quality inspection defects", "QLT-01"), ("batch identifier", "QLT-01"),
    ("deployment rollback", "REL-01"), ("release version", "REL-01"),
    ("cafeteria menu", None), ("payroll schedule", None), ("parking permits", None),
    ("", None),
]


class Assistant:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.index = self.vectorizer.fit_transform(DOCS.values())

    def answer(self, question):
        query = self.vectorizer.transform([question])
        scores = (self.index @ query.T).toarray().ravel()
        best = int(scores.argmax())
        if scores[best] < .15:
            return {"citation": None, "excerpt": None, "manual_review": True}
        source = list(DOCS)[best]
        return {"citation": source, "excerpt": DOCS[source], "manual_review": False}


def evaluate(assistant):
    results = []
    for question, expected in CASES:
        outcome = assistant.answer(question)
        passed = (outcome["citation"] == expected and
                  outcome["manual_review"] == (expected is None) and
                  outcome["excerpt"] == DOCS.get(expected))
        results.append({"question": question, "expected": expected,
                        "actual": outcome["citation"], "passed": passed})
    return {"passed": sum(row["passed"] for row in results),
            "total": len(results), "cases": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?")
    args = parser.parse_args()
    assistant = Assistant()
    result = assistant.answer(args.question) if args.question is not None else evaluate(assistant)
    print(json.dumps(result, indent=2))
    if args.question is None and result["passed"] != result["total"]:
        raise SystemExit(1)
