# AI / Machine Learning / Data Science Portfolio

[← Back to GitHub profile](../README.md)

This is the **project directory** for seven runnable examples. Each folder has a README, Python source code, and unit tests. Projects use **synthetic data** or a tiny local knowledge base; none claims access to employer data.

## 🤖 Machine learning and AI applications

| Project | Main skill | Recruiter-friendly summary |
| --- | --- | --- |
| [Industrial predictive maintenance](industrial-maintenance/) | ML classification | Train a logistic regression model on simulated equipment readings and evaluate failure-risk alerts |
| [Contextual Q&A application](llm-qa-api/) | LLM software design | Retrieve passages, construct grounded prompts, support injectable model clients and test fallback paths |

## 📊 Data science and product analytics

| Project | Main skill | Recruiter-friendly summary |
| --- | --- | --- |
| [Telecom customer churn](telecom-churn/) | Retention analytics | Compare churn across service-contact and contract cohorts |
| [A/B testing and product experiments](product-experimentation/) | Experiment statistics | Calculate variant conversion, absolute lift and confidence intervals |
| [Retail demand forecasting](retail-demand-forecast/) | Forecasting | Evaluate a weekly seasonal-naive baseline using MAE, RMSE and WAPE |

## 🏦 Industry-specific analytics

| Project | Main skill | Recruiter-friendly summary |
| --- | --- | --- |
| [Financial transaction risk](fintech-transaction-risk/) | Risk analysis | Test an interpretable alerting heuristic, precision and recall |
| [Healthcare readmission analysis](healthcare-readmission/) | Healthcare analytics | Analyze 30-day readmission rates by synthetic prior-utilization cohorts |

## 🛠️ How to navigate

Choose any project above → open its **README.md** for an overview → open the main **.py** file for the implementation → open **test_*.py** for tests.

To run an individual project, follow its README. To run all project tests from the profile repository root:

```bash
for project in portfolio/*; do
  if [ -d "$project" ] && ls "$project"/test_*.py >/dev/null 2>&1; then
    python -m unittest discover -s "$project" -p 'test_*.py' -v
  fi
done
```

**Automated checks:** [GitHub Actions](../../actions) — workflows test the portfolio when the relevant files change and on a maintenance schedule. Scheduled CI is not a substitute for actual development work.

## 🔭 Next improvements

Add realistic data sources where permitted, stronger validation and benchmarks, dashboards, model calibration, and deployed API demonstrations. These examples are a foundation for deeper, individually showcased projects.

**Data disclosure:** All demo datasets are simulated; metrics are reproducible demonstration outputs, not production results or company-specific achievements.
