"""Patient readmission cohort analysis using synthetic healthcare records."""
from collections import defaultdict
from random import Random


def make_encounters(n=1000, seed=13):
    rng = Random(seed)
    encounters = []
    for i in range(n):
        age = rng.randrange(18, 91)
        previous_admissions = rng.randrange(0, 6)
        length_of_stay = rng.randrange(1, 16)
        followup = int(rng.random() < 0.65)
        # Simulated outcome, not a clinical or deployable prediction model.
        probability = min(0.85, 0.06 + 0.07 * previous_admissions
                          + 0.09 * (length_of_stay > 10)
                          + 0.07 * (age > 75) - 0.03 * followup)
        encounters.append({"encounter_id": i, "age": age,
                           "prior_admissions": previous_admissions,
                           "length_of_stay": length_of_stay,
                           "followup_scheduled": followup,
                           "readmitted_30d": int(rng.random() < probability)})
    return encounters


def cohort_readmission_rates(records):
    seen = set()
    groups = defaultdict(lambda: {"n": 0, "readmissions": 0})
    for row in records:
        if row["encounter_id"] in seen:
            raise ValueError("Duplicate encounter")
        seen.add(row["encounter_id"])
        if row["readmitted_30d"] not in (0, 1):
            raise ValueError("Unexpected outcome")
        group = "high_prior_utilization" if row["prior_admissions"] >= 3 else "low_prior_utilization"
        groups[group]["n"] += 1
        groups[group]["readmissions"] += row["readmitted_30d"]
    if not groups:
        raise ValueError("No encounters provided")
    return {name: {"encounters": data["n"],
                   "readmission_rate": data["readmissions"] / data["n"]}
            for name, data in sorted(groups.items())}


if __name__ == "__main__":
    report = cohort_readmission_rates(make_encounters())
    print("SYNTHETIC DEMO: 30-day readmission cohorts")
    for group, values in report.items():
        print(f"{group}: n={values['encounters']}, "
              f"readmission_rate={values['readmission_rate']:.1%}")
    print("Not for clinical decision-making; cohort differences are not causal.")
