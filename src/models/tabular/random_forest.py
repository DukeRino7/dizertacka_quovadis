"""Random Forest – klasický súbor rozhodovacích stromov."""
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from .base import TabularModel


class RandomForest(TabularModel):
    name = "random_forest"

    def fit(self, X, y, w, X_val, y_val):
        p = self.params
        self.model = RandomForestClassifier(
            n_estimators=p["n_estimators"], max_depth=p.get("max_depth"), min_samples_leaf=p["min_samples_leaf"],
            max_features=p["max_features"], n_jobs=self.threads, random_state=self.seed)
        self.model.fit(X, y, sample_weight=w)
        return {}

    def predict_proba(self, X):
        self.model.n_jobs = self.threads
        return self.model.predict_proba(X)[:, 1]

    def n_parameters(self):
        return int(sum(t.tree_.node_count for t in self.model.estimators_))

    def _save(self, path: Path):
        joblib.dump(self.model, path / "model.joblib")

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"]); m.model = joblib.load(path / "model.joblib"); return m
