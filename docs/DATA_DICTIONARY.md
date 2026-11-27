# Data Dictionary

| Field | Meaning | Notes |
|---|---|---|
| Time | Seconds elapsed from a reference point | Not wall-clock date/time; interpret as relative time only |
| V1-V28 | PCA-transformed anonymized numeric features | Semantic meanings are not provided in the benchmark |
| Amount | Transaction amount | Dataset currency/context should be taken from source documentation |
| Class | Ground-truth label | 0 = legitimate, 1 = fraud |
| source_row_id | 1-based row number from the original CSV | Retained after exact-duplicate removal for Python-to-Oracle reconciliation |

Derived fields:

| Field | Meaning |
|---|---|
| rule_high_amount | Amount exceeds training-set quantile threshold |
| rule_feature_outlier | Sum of absolute V1-V28 values exceeds training threshold |
| rule_time_bucket_density_proxy | Count of all dataset rows in its time bucket exceeds training-set threshold; not card-level velocity |
| rules_triggered | Number of the three flags raised |
| rule_flag | At least one rule raised |
