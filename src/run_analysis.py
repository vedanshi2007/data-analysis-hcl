"""Run data profiling, train-calibrated rules and holdout evaluation."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from .config import AMOUNT_QUANTILE, FEATURE_MAGNITUDE_QUANTILE, TIME_BUCKET_COUNT_QUANTILE, TIME_BUCKET_SECONDS, HOLDOUT_FRACTION
from .rules import fit_rule_thresholds, apply_rules, FEATURE_COLUMNS
from .metrics import evaluate_flags

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/creditcard.csv')
    parser.add_argument('--output', default='reports')
    args = parser.parse_args()
    path, out_dir = Path(args.input), Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        raise SystemExit(f"Dataset not found: {path}. See README.md for download instructions.")
    df = pd.read_csv(path)
    required = {'Time', 'Amount', 'Class', *FEATURE_COLUMNS}
    missing = required.difference(df.columns)
    if missing: raise SystemExit(f"Dataset schema mismatch; missing: {sorted(missing)}")
    if df.empty: raise SystemExit('Dataset contains no rows.')
    duplicate_rows_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    df['Class'] = pd.to_numeric(df['Class'], errors='raise').astype(int)
    if not set(df['Class'].unique()).issubset({0, 1}): raise SystemExit('Class must contain only 0/1.')
    df = df.sort_values('Time', kind='stable').reset_index(drop=True)
    split = max(1, int(len(df) * (1 - HOLDOUT_FRACTION)))
    train, holdout = df.iloc[:split].copy(), df.iloc[split:].copy()
    if holdout.empty: raise SystemExit('Not enough rows for a holdout segment.')
    thresholds = fit_rule_thresholds(train, AMOUNT_QUANTILE, FEATURE_MAGNITUDE_QUANTILE, TIME_BUCKET_COUNT_QUANTILE, TIME_BUCKET_SECONDS)
    scored = apply_rules(holdout, thresholds)
    metrics = evaluate_flags(scored['Class'], scored['rule_flag'])
    metrics.update({
        'dataset_rows_after_exact_deduplication': int(len(df)),
        'exact_duplicate_rows_removed': duplicate_rows_removed,
        'calibration_rows': int(len(train)), 'holdout_rows': int(len(holdout)),
        'holdout_start_time_seconds': float(holdout['Time'].min()),
        'holdout_end_time_seconds': float(holdout['Time'].max()),
        'fraud_prevalence_holdout': float(holdout['Class'].mean()),
        'thresholds': thresholds,
        'note': 'Time-ordered holdout; simple rule baseline; time density is a dataset-level proxy, not card-level velocity.'
    })
    quality = pd.DataFrame({
        'column': df.columns,
        'dtype': [str(df[c].dtype) for c in df.columns],
        'missing_count': [int(df[c].isna().sum()) for c in df.columns],
        'missing_pct': [float(df[c].isna().mean()*100) for c in df.columns],
        'distinct_count': [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    quality.to_csv(out_dir/'data_quality_profile.csv', index=False)
    scored.to_csv(out_dir/'holdout_flagged_transactions.csv', index=False)
    pd.DataFrame([metrics]).to_json(out_dir/'evaluation_summary.json', orient='records', indent=2)
    pd.DataFrame([{'metric': k, 'value': v} for k, v in metrics.items() if isinstance(v, (int, float))]).to_csv(out_dir/'evaluation_summary.csv', index=False)
    rule_summary = pd.DataFrame([
        {'rule':'High transaction amount','flagged_count':int(scored['rule_high_amount'].sum())},
        {'rule':'Anonymized-feature outlier','flagged_count':int(scored['rule_feature_outlier'].sum())},
        {'rule':'Time-bucket density proxy','flagged_count':int(scored['rule_time_bucket_density_proxy'].sum())},
        {'rule':'Any rule','flagged_count':int(scored['rule_flag'].sum())},
    ])
    rule_summary.to_csv(out_dir/'rule_summary.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    counts = scored['Class'].value_counts().reindex([0,1], fill_value=0)
    axes[0].bar(['Legitimate','Fraud'], counts.values)
    axes[0].set_title('Actual labels - holdout'); axes[0].set_ylabel('Transactions')
    axes[1].bar(['Precision','Recall','F1'], [metrics['precision'], metrics['recall'], metrics['f1']])
    axes[1].set_ylim(0,1); axes[1].set_title('Rule baseline performance')
    fig.tight_layout(); fig.savefig(out_dir/'holdout_performance.png', dpi=160); plt.close(fig)
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__': main()
