"""Detekčné metriky pre binárnu úlohu malware (1) / benign (0).

Skóre = pravdepodobnosť triedy malware. Rozhodnutie: malware, ak skóre >= prah.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, brier_score_loss, log_loss, matthews_corrcoef,
                             roc_auc_score, roc_curve)


def threshold_free(y: np.ndarray, s: np.ndarray, tpr_at: list[float]) -> dict:
    s = np.clip(s, 1e-7, 1 - 1e-7)
    out = {
        "roc_auc": roc_auc_score(y, s),
        "pr_auc": average_precision_score(y, s),
        "log_loss": log_loss(y, s),
        "brier": brier_score_loss(y, s),
    }
    fpr, tpr, _ = roc_curve(y, s)
    for f in tpr_at:
        out[f"tpr_at_fpr_{f:g}"] = float(np.max(tpr[fpr <= f])) if np.any(fpr <= f) else 0.0
    return out


def threshold_for_fpr(y: np.ndarray, s: np.ndarray, target_fpr: float) -> float:
    """Najnižší prah, pri ktorom FPR <= target_fpr (t. j. najvyššie TPR pri danom obmedzení)."""
    fpr, _, thr = roc_curve(y, s)
    ok = np.flatnonzero(fpr <= target_fpr)
    return float(min(thr[ok[-1]], 1.0))


def at_threshold(y: np.ndarray, s: np.ndarray, thr: float) -> dict:
    p = (s >= thr).astype(int)
    tp = int(((p == 1) & (y == 1)).sum()); fp = int(((p == 1) & (y == 0)).sum())
    tn = int(((p == 0) & (y == 0)).sum()); fn = int(((p == 0) & (y == 1)).sum())
    tpr = tp / max(tp + fn, 1); fpr = fp / max(fp + tn, 1)
    prec = tp / max(tp + fp, 1)
    return {
        "threshold": thr, "accuracy": (tp + tn) / len(y), "balanced_accuracy": (tpr + 1 - fpr) / 2,
        "precision": prec, "recall_tpr": tpr, "fpr": fpr, "fnr": 1 - tpr,
        "f1": 2 * prec * tpr / max(prec + tpr, 1e-12), "mcc": matthews_corrcoef(y, p),
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
    }


def per_family(meta: pd.DataFrame, s: np.ndarray, thr: float) -> pd.DataFrame:
    """Podiel vzoriek označených ako malware v každej rodine (pri benign = FPR, inak detekcia)."""
    d = meta.assign(pred=(s >= thr).astype(int))
    return d.groupby("family")["pred"].agg(n="size", detected_rate="mean").reset_index()


def evaluate(y, s, thresholds: dict, tpr_at: list[float], meta: pd.DataFrame | None = None) -> dict:
    out = {"n": int(len(y)), "malware_share": float(np.mean(y)), **threshold_free(y, s, tpr_at)}
    for name, thr in thresholds.items():
        out[f"at_{name}"] = at_threshold(y, s, thr)
        if meta is not None:
            out[f"at_{name}"]["per_family"] = per_family(meta, s, thr).to_dict(orient="records")
    return out
