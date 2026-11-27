"""Explainable rule flags; thresholds are learned on a calibration subset."""
from __future__ import annotations
import pandas as pd

FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)]

def fit_rule_thresholds(train: pd.DataFrame, amount_q: float, feature_q: float,
                        time_count_q: float, bucket_seconds: int) -> dict:
    required = {"Amount", "Time", *FEATURE_COLUMNS}
    missing = required.difference(train.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    bucket = (pd.to_numeric(train["Time"], errors="coerce") // bucket_seconds).astype("Int64")
    bucket_counts = bucket.value_counts(dropna=True)
    return {
        "amount_threshold": float(train["Amount"].quantile(amount_q)),
        "feature_magnitude_threshold": float(train[FEATURE_COLUMNS].abs().sum(axis=1).quantile(feature_q)),
        "time_bucket_count_threshold": float(bucket_counts.quantile(time_count_q)) if len(bucket_counts) else float("inf"),
        "bucket_seconds": int(bucket_seconds),
    }

def apply_rules(frame: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
    out = frame.copy()
    bucket = (pd.to_numeric(out["Time"], errors="coerce") // thresholds["bucket_seconds"]).astype("Int64")
    bucket_counts = bucket.map(bucket.value_counts(dropna=True)).fillna(0)
    feature_magnitude = out[FEATURE_COLUMNS].abs().sum(axis=1)
    out["rule_high_amount"] = out["Amount"] > thresholds["amount_threshold"]
    out["rule_feature_outlier"] = feature_magnitude > thresholds["feature_magnitude_threshold"]
    # Dataset time-bucket density proxy; NOT a card-level velocity rule.
    out["rule_time_bucket_density_proxy"] = bucket_counts > thresholds["time_bucket_count_threshold"]
    rule_cols = ["rule_high_amount", "rule_feature_outlier", "rule_time_bucket_density_proxy"]
    out["rules_triggered"] = out[rule_cols].sum(axis=1).astype(int)
    out["rule_flag"] = out["rules_triggered"] >= 1
    return out
