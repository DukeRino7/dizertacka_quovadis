"""Logistická regresia (L2) – najľahší lineárny model rebríčka."""
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from .base import TabularModel


class LogReg(TabularModel):
    name = "logreg"
    needs_scaling = True

    def fit(self, X, y, w, X_val, y_val):
        self.model = LogisticRegression(C=self.params["C"], solver="lbfgs", max_iter=self.params.get("max_iter", 2000),
                                        random_state=self.seed)
        self.model.fit(X, y, sample_weight=w)
        return {"n_iter": int(self.model.n_iter_[0])}

    def predict_proba(self, X):
        z = np.asarray(X, dtype=np.float64) @ self.model.coef_[0] + self.model.intercept_[0]
        return 1.0 / (1.0 + np.exp(-z))

    def n_parameters(self):
        return int(self.model.coef_.size + self.model.intercept_.size)

    def _save(self, path: Path):
        joblib.dump(self.model, path / "model.joblib")

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"]); m.model = joblib.load(path / "model.joblib"); return m
