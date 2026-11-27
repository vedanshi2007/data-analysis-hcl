# Credit Card Transaction and Fraud Pattern Analysis

**Project:** Project 7 from the II Year Data Analyst Project List  
**Domain:** Banking and Finance  
**Stack:** Python, Oracle SQL, Power BI

## Objective
Build a reproducible workflow that profiles credit-card transactions, applies transparent rule-based anomaly flags, evaluates those flags against known labels, and prepares outputs for a fraud-monitoring dashboard.

## Data
Download the Kaggle ULB Credit Card Fraud Detection dataset and place `creditcard.csv` in `data/`. The public benchmark uses `Time`, `V1`-`V28`, `Amount`, and `Class` (1 = fraud). The repository does not redistribute source data. Review source terms before use: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

## Project layout
- `src/`: Python profiling, rule flags, evaluation and runner
- `sql/`: Oracle DDL, loading notes and analysis queries
- `powerbi/`: Power BI page plan and DAX measure guide
- `docs/`: project brief, data dictionary and methodology
- `tests/`: unit tests
- `reports/`: generated outputs (not pre-filled with invented results)
- `.github/workflows/`: automated Python unit-test workflow

## Setup and execution
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_analysis --input data/creditcard.csv --output reports
python -m unittest discover -s tests -v
```

## Implemented fraud flags
1. Amount above a training-derived high quantile.
2. An unusually high absolute-magnitude aggregate across anonymized PCA features `V1`-`V28`.
3. A dataset-wide time-bucket density proxy. The benchmark has no card identifier, so this is explicitly **not** card-level velocity detection.

Thresholds are calibrated on the earlier time-ordered segment and evaluated on a later holdout. Metrics include precision, recall, F1 and confusion counts. The rules are explainable baselines, not production fraud decisions.

## Oracle and Power BI
Oracle SQL setup is in `sql/`. Power BI dashboard guidance and DAX are in `powerbi/POWER_BI_GUIDE.md`. A `.pbix` file is not included; build and save it in Power BI Desktop from the generated CSV outputs.

## Caveats
The benchmark's V-features are anonymized PCA transformations; no named merchant, cardholder or issuer features are available. `Time` is relative elapsed seconds, not a calendar timestamp, so calendar-midnight claims cannot be derived from it. Actual metrics are intentionally left unreported until the dataset is downloaded and the workflow is run.
