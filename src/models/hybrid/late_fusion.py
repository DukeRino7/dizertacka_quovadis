"""Neskorá fúzia: spojenie skóre statického a dynamického modelu pre KAŽDÚ vzorku (hybridný baseline).

Metódy:
- mean     : priemer pravdepodobností (nič sa neučí),
- stacking : logistická regresia nad logitmi oboch skóre, učená na VALIDÁCII; skóre validácie sa počítajú
             krížovo (5 častí), aby prah určený na validácii nebol optimistický; test sa iba transformuje.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict


def _logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def fuse(method: str, s_val: tuple, s_test: tuple, y_val: np.ndarray, seed: int = 0):
    """s_val/s_test = (skóre statické, skóre dynamické). Vráti (skóre validácie, skóre testu)."""
    if method == "mean":
        return (s_val[0] + s_val[1]) / 2, (s_test[0] + s_test[1]) / 2
    if method == "stacking":
        Zv = np.column_stack([_logit(s) for s in s_val]); Zt = np.column_stack([_logit(s) for s in s_test])
        lr = LogisticRegression(C=1.0, max_iter=1000)
        cv = StratifiedKFold(5, shuffle=True, random_state=seed)
        val = cross_val_predict(lr, Zv, y_val, cv=cv, method="predict_proba")[:, 1]
        test = lr.fit(Zv, y_val).predict_proba(Zt)[:, 1]
        return val, test
    raise ValueError(method)
