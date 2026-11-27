# Methodology and Evaluation Protocol

1. Read the Kaggle CSV and validate required schema (`Time`, `V1`-`V28`, `Amount`, `Class`).
2. Remove exact duplicate rows; report retained row count. This is exact-row deduplication, not entity resolution.
3. Sort observations by relative `Time` and reserve the final 20% as a time-ordered holdout.
4. Learn rule thresholds on the earlier calibration segment only.
5. Apply thresholds unchanged to the holdout.
6. Compare binary rule flags with `Class`; report precision, recall, F1 and confusion counts.
7. Export row-level holdout flags and supporting summary files.

## Metric definitions
- Precision = TP / (TP + FP): share of flagged transactions that are truly fraud.
- Recall = TP / (TP + FN): share of actual fraud transactions that are flagged.
- F1 = harmonic mean of precision and recall.

A low-prevalence dataset makes accuracy potentially misleading, so precision and recall are emphasized. A threshold baseline is a transparent analytical starting point, not a production classifier.

## Limitations
The third rule is a dataset-wide time-bucket density proxy because the benchmark does not provide a card identifier. It cannot support card-specific velocity claims. PCA-transformed features are not human-interpretable fields. Do not interpret the result as production-ready fraud screening.
