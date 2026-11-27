"""Evaluation metrics for binary fraud flags."""
from __future__ import annotations
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

def evaluate_flags(y_true, y_pred) -> dict:
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "precision": float(precision), "recall": float(recall), "f1": float(f1),
        "true_negative": int(tn), "false_positive": int(fp),
        "false_negative": int(fn), "true_positive": int(tp),
        "actual_fraud": int(tp + fn), "flagged_transactions": int(tp + fp),
    }
