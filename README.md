# Niranjanaa Jayakumar

I'm an M.S. in Artificial Intelligence student at **Kennesaw State University** (expected December 2027). I work on AI applications that retrieve useful information, connect to existing systems, and make their outputs easier to verify. I'm based in Atlanta and exploring Summer 2027 internships in AI engineering, machine learning, and data science.

[LinkedIn](https://www.linkedin.com/in/niranjanaa-jayakumar-32584721a/) · [Email](mailto:jkniranjanaa@gmail.com) · [All projects](portfolio/README.md)

## Current research

At KSU's **HEART Lab**, I built and deployed the Mind Your Heart research website. My current work explores how LLM-assisted retrieval and interaction tracking could support a digital health research study.

## Featured AI engineering projects

| Project | What it does | Explore |
| --- | --- | --- |
| **Runbook Investigation Agent** | Uses LLM tool calling to pull incident evidence from a Python REST API and retrieve troubleshooting guidance from SQLite. Returns source IDs and falls back to structured evidence if citations are missing. | [Run instructions](portfolio/nonproduction-incident-investigation/README.md#2-runbook-investigation-agent) · [Agent code](portfolio/nonproduction-incident-investigation/agent.py) |
| **Incident Trends API** | Groups synthetic nonproduction incidents by service and ranks recurring failure signatures. Returns structured JSON for investigation. | [Run instructions](portfolio/nonproduction-incident-investigation/README.md#1-incident-trends-api) · [API code](portfolio/nonproduction-incident-investigation/incident_api.py) |
| **Contextual AI Q&A** | Retrieves relevant passages, builds grounded prompts, and tests how the application behaves when the model is unavailable. | [README and code](portfolio/llm-qa-api/) |

The two incident projects share a [test suite](portfolio/nonproduction-incident-investigation/test_portfolio.py) and run on synthetic data. The agent has a local retrieval mode, and its LLM tool-call path is covered by tests with a simulated provider.

## Machine learning and analytics

| Project | What it demonstrates |
| --- | --- |
| [Industrial Predictive Maintenance](portfolio/industrial-maintenance/) | Classify equipment failure risk from simulated sensor readings and evaluate the model on holdout data. |
| [Telecom Churn Analytics](portfolio/telecom-churn/) | Compare churn across subscriber and contract segments. |
| [Product Experimentation](portfolio/product-experimentation/) | Estimate conversion lift and confidence intervals from simulated A/B tests. |
| [Retail Demand Forecasting](portfolio/retail-demand-forecast/) | Benchmark seasonal forecasts and compare error metrics. |
| [Transaction Risk Triage](portfolio/fintech-transaction-risk/) | Evaluate explainable risk scoring and alert metrics. |
| [Healthcare Readmission Analysis](portfolio/healthcare-readmission/) | Analyze 30-day readmission rates across synthetic patient cohorts. |

## Technical skills

**Programming & analytics:** Python, SQL, Pandas, NumPy, data visualization  
**Machine learning:** scikit-learn, classification, regression, model evaluation, statistics  
**AI & engineering:** LLM applications, REST APIs, Git, automated unit testing

## Education and certifications

- **M.S. Artificial Intelligence** — Kennesaw State University (expected Dec 2027)
- **B.S. Information Technology (Data Analytics)** — Kennesaw State University (May 2025)
- AWS Certified Machine Learning Engineer – Associate
- Google Advanced Data Analytics Professional Certificate
- Generative AI with Large Language Models — DeepLearning.AI & AWS
