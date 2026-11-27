# Power BI Dashboard Build Guide

Load the generated files from `reports/` after running the Python workflow:
- `holdout_flagged_transactions.csv`
- `rule_summary.csv`
- `data_quality_profile.csv`
- `evaluation_summary.csv` (optional KPI audit/export)

## Suggested pages

### Fraud Overview
Cards: transaction count, actual fraud count, flagged transactions, precision, recall and F1. Add actual fraud vs legitimate, flagged vs not flagged, and slicers for actual label and rule flag.

### Rule Performance
Bar chart of flagged count by rule, a matrix of `rule_flag` by `Class`, and a table of false positives and false negatives.

### Transaction Exploration
Table of Time, Amount, Class, individual rule flags and rules_triggered. Scatter plot of Amount by Time.

## DAX measures
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

Check imported boolean types in Power Query. The .pbix is not part of this repository; build it in Power BI Desktop and save it as `powerbi/credit_card_fraud_dashboard.pbix`.
