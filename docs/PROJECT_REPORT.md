# Credit Card Transaction and Fraud Pattern Analysis — Project Report

**Domain:** Banking and Finance  
**Stack:** Python, Oracle SQL, Power BI  
**Repository:** https://github.com/vedanshi2007/data-analysis-hcl

## Executive summary
This project profiles labelled credit-card transaction data, removes exact duplicate rows, applies three explainable anomaly flags, and evaluates the combined rule baseline on a time-ordered holdout. It includes Oracle SQL schema and analysis queries, a Power BI dashboard guide, tests, and a reproducible Python runner.

## Problem and objectives
Financial institutions need to detect suspicious transactions while controlling false alerts. This educational project demonstrates data validation, rule-based anomaly detection, imbalanced-class evaluation, SQL analysis and dashboard design. It is not a production fraud-decision system.

## Dataset
Download the Kaggle ULB Credit Card Fraud Detection dataset from https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud and place `creditcard.csv` in `data/`. The dataset includes `Time`, `V1`–`V28`, `Amount` and `Class` (0 = legitimate, 1 = fraud). V1–V28 are anonymized PCA features. Time is elapsed seconds, not a calendar timestamp.

## Implemented rules
1. **High amount:** Amount above the calibration-set 99.5th percentile.
2. **Feature outlier:** Sum of absolute V1–V28 values above the calibration-set 99.5th percentile.
3. **Time-bucket density proxy:** Flag rows in elapsed-time buckets whose count exceeds the calibration-set 99.5th percentile of bucket counts. This is dataset-wide activity, not card-level velocity; no card identifier exists in this benchmark.

The earlier 80% of time-sorted rows calibrates thresholds; the final 20% is the holdout. Exact duplicate rows are removed, while `source_row_id` preserves the original CSV position for Oracle reconciliation.

## Evaluation
The pipeline reports precision, recall, F1 and true-negative, false-positive, false-negative and true-positive counts. Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 is their harmonic mean. Accuracy alone is not emphasized because the fraud class is imbalanced.

**No numerical results are asserted in this document.** Run the pipeline against the downloaded dataset to generate measured results in `reports/`. Do not invent metrics.

## Python workflow
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_analysis --input data/creditcard.csv --output reports
python -m unittest discover -s tests -v
```

Generated outputs include data quality profile, row-level holdout flags, rule summary, evaluation summary (CSV/JSON) and a performance chart.

## Oracle SQL
- `sql/01_create_tables.sql`: transaction and flag-result tables, constraints and indexes.
- `sql/02_load_instructions.sql`: staging and secure load guidance.
- `sql/03_analysis_queries.sql`: fraud prevalence, amount profiles, relative-time buckets, analytic activity window and confusion counts.

The rolling activity query is dataset-wide. It must not be presented as card-level velocity. Never commit database credentials or real cardholder data.

## Power BI dashboard
Use `powerbi/POWER_BI_GUIDE.md` to build:
- **Fraud Overview:** volume, actual fraud, flagged transactions, precision, recall and F1.
- **Rule Performance:** flagged count by rule, confusion matrix and false-positive/false-negative review.
- **Transaction Exploration:** amount/time scatter plot and row-level flags.

The repository contains the dashboard build guide and DAX measures, not a finished `.pbix` file.

## Limitations and responsible use
- Rules are simple quantile-based baselines, not production classifiers.
- V1–V28 have no directly interpretable business labels.
- No card identifier means per-card velocity cannot be calculated.
- Elapsed Time cannot establish calendar midnight or timezone behavior.
- Benchmark performance may not generalize to a live portfolio.

## Acceptance checklist
- [x] Three explainable rule flags
- [x] Label comparison and precision/recall/F1 calculation
- [x] Exact duplicate handling
- [x] Imbalanced-class-aware reporting
- [x] Oracle DDL and analytical SQL
- [x] Power BI dashboard guide and DAX
- [x] Python unit tests and GitHub Actions workflow
- [ ] Run against the actual CSV and review measured results
- [ ] Build and save the Power BI `.pbix` dashboard

## Project PDF
A detailed PDF report is provided separately for review. Repository source: https://github.com/vedanshi2007/data-analysis-hcl
