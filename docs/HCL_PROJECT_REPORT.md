# Credit Card Transaction and Fraud Pattern Analysis — Project Report

**Project:** Project 7 — Data Analyst Project List  
**Domain:** Banking and Finance  
**Stack:** Python, Oracle SQL, Power BI  
**Repository:** https://github.com/vedanshi2007/data-analysis-hcl

## 1. Executive summary

This project demonstrates a reproducible fraud-analysis workflow using a labelled credit-card transaction benchmark. It profiles data quality, removes exact duplicate records, calibrates three explainable anomaly rules on an earlier time segment, evaluates the combined flag on a later holdout, prepares Oracle SQL analysis and defines a Power BI monitoring dashboard.

**Results status:** Numerical results are generated only after the source CSV is downloaded and the workflow is run. No precision, recall, fraud count or dashboard outcome is fabricated.

## 2. Problem statement

Financial institutions need to identify suspicious payment activity while controlling false alerts. False positives consume investigation effort; missed fraud creates financial and customer impact. This project provides an educational, explainable baseline—not a production fraud-decision system.

## 3. Dataset

Source: [Kaggle ULB Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Download `creditcard.csv` into `data/`. The dataset is not redistributed in this repository.

| Field | Meaning |
|---|---|
| `Time` | Seconds elapsed from a reference point; not a calendar timestamp |
| `V1`–`V28` | Anonymized PCA-transformed numeric features |
| `Amount` | Transaction amount |
| `Class` | Label: 0 = legitimate, 1 = fraud |
| `source_row_id` | Original CSV row position for Python/Oracle reconciliation |

The V-features have no supplied business semantics. The Time field cannot establish local time, timezone or calendar midnight.

## 4. Workflow

1. Read the CSV and validate required columns, non-empty rows and binary labels.
2. Add a stable original-row key and remove exact duplicate transaction rows.
3. Sort by elapsed Time and reserve the final 20% as a time-ordered holdout.
4. Fit thresholds using only the earlier calibration segment.
5. Apply unchanged thresholds to the holdout and compare flags with `Class`.
6. Export data quality, transaction flags, rule counts, evaluation metrics and a performance chart.
7. Load data and flags into Oracle and build the Power BI report using the supplied guide.

## 5. Fraud detection rules

### Rule 1 — High transaction amount
Flag `Amount` above the 99.5th percentile calculated from the calibration segment.

### Rule 2 — Anonymized-feature magnitude outlier
Calculate the sum of absolute values across V1–V28 and flag values above the calibration-set 99.5th percentile. This is a generic outlier heuristic, not a semantic interpretation of the PCA features.

### Rule 3 — Time-bucket density proxy
Group observations into numeric 3,600-second elapsed-time buckets and flag rows in buckets whose counts exceed the calibration-set 99.5th percentile of bucket counts. This is a dataset-wide activity-density proxy, **not card-level velocity**, because the source has no card identifier.

A transaction is flagged when one or more rules fire. Individual flags and the number of triggered rules are retained for explainability.

## 6. Evaluation

The final 20% of time-ordered observations form the holdout. Thresholds are learned on the earlier segment only.

- **Precision** = TP / (TP + FP): share of flagged transactions that are fraud.
- **Recall** = TP / (TP + FN): share of actual fraud transactions that are flagged.
- **F1** = harmonic mean of precision and recall.
- Confusion counts: true positives, false positives, false negatives and true negatives.

Because fraud is a minority class, precision, recall and F1 are emphasized over accuracy alone.

Generated outputs:
- `reports/data_quality_profile.csv`
- `reports/holdout_flagged_transactions.csv`
- `reports/evaluation_summary.json`
- `reports/evaluation_summary.csv`
- `reports/rule_summary.csv`
- `reports/holdout_performance.png`

## 7. Duplicate handling and time edge cases

Exact duplicate rows are removed based on transaction fields, excluding the generated `source_row_id`. This is not customer or transaction-entity resolution. The source row key supports reconciliation after sorting.

Because Time is elapsed seconds, the project uses numeric buckets and avoids calendar timestamp conversion. A true midnight edge case requires a real timestamp and timezone policy; it cannot be inferred from this benchmark.

## 8. Oracle SQL

- `sql/01_create_tables.sql`: creates transaction and rule-result tables with a unique source row key, binary-label constraints and indexes.
- `sql/02_load_instructions.sql`: describes CSV staging and secure loading.
- `sql/03_analysis_queries.sql`: transaction/fraud prevalence, amount profiles, elapsed-time buckets, analytic activity windows and confusion counts.

The rolling activity query is a dataset-wide proxy, not per-card velocity. Never commit credentials or sensitive cardholder data.

## 9. Power BI dashboard

See [Power BI Dashboard Build Guide](../powerbi/POWER_BI_GUIDE.md).

Suggested pages:
- **Fraud Overview:** transaction count, actual fraud count, flagged count, precision, recall, F1, label distribution and flagged/unflagged comparison.
- **Rule Performance:** flagged count by rule, confusion matrix, false-positive and false-negative review.
- **Transaction Exploration:** Time, Amount, Class, rule flags and rules_triggered; Amount vs Time scatter plot.

Core measures:

```DAX
Transactions = COUNTROWS('holdout_flagged_transactions')
Actual Fraud = CALCULATE([Transactions], 'holdout_flagged_transactions'[Class] = 1)
Flagged Transactions = CALCULATE([Transactions], 'holdout_flagged_transactions'[rule_flag] = TRUE())
True Positive = CALCULATE([Transactions], 'holdout_flagged_transactions'[Class] = 1, 'holdout_flagged_transactions'[rule_flag] = TRUE())
False Positive = CALCULATE([Transactions], 'holdout_flagged_transactions'[Class] = 0, 'holdout_flagged_transactions'[rule_flag] = TRUE())
False Negative = CALCULATE([Transactions], 'holdout_flagged_transactions'[Class] = 1, 'holdout_flagged_transactions'[rule_flag] = FALSE())
Precision = DIVIDE([True Positive], [True Positive] + [False Positive], 0)
Recall = DIVIDE([True Positive], [True Positive] + [False Negative], 0)
F1 = DIVIDE(2 * [Precision] * [Recall], [Precision] + [Recall], 0)
```

A finished .pbix is not included; build it in Power BI Desktop from generated outputs.

## 10. Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Download creditcard.csv into data/
python -m src.run_analysis --input data/creditcard.csv --output reports
python -m unittest discover -s tests -v
```

## 11. Limitations and responsible use

- Metrics remain pending until the actual dataset is processed.
- Quantile rules are transparent baselines, not a trained production model.
- No card identifier is available for card-level velocity.
- PCA features are anonymized and not human-interpretable.
- Elapsed Time is not a calendar timestamp.
- Benchmark results may not generalize to a live card portfolio.
- Operational decisions require validation, governance and human review.

## 12. Completion checklist

- Python profiling, rule flags and holdout evaluation.
- Oracle schema, loading notes and analytical SQL.
- Power BI page design and DAX guide.
- Data dictionary, methodology and project brief.
- Unit tests and GitHub Actions workflow.
- PDF report available as a separate downloadable deliverable.

Before presenting, download the dataset, execute the pipeline, review measured metrics, build the .pbix dashboard and update the report with actual findings.

---
**Repository:** https://github.com/vedanshi2007/data-analysis-hcl  
**Dataset:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
