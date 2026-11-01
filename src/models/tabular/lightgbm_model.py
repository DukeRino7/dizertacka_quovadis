"""LightGBM – gradient boosting rozhodovacích stromov s early stopping na validácii."""
from pathlib import Path

import lightgbm as lgb
import numpy as np

from .base import TabularModel

_DATASET_CACHE: dict = {}  # opakované pokusy ladenia použijú rovnako zbinované dáta


def _dataset(X, y, w, reference=None):
    key = (id(X), len(X), id(w))
    if key not in _DATASET_CACHE:
        if len(_DATASET_CACHE) > 4:
            _DATASET_CACHE.clear()
        _DATASET_CACHE[key] = lgb.Dataset(X, label=y, weight=w, reference=reference, free_raw_data=False,
                                          params={"feature_pre_filter": False, "verbose": -1})
    return _DATASET_CACHE[key]


class LightGBM(TabularModel):
    name = "lightgbm"

    def fit(self, X, y, w, X_val, y_val):
        p = dict(self.params)
        rounds = p.pop("num_boost_round", 5000)
        patience = p.pop("early_stopping_rounds", 100)
        params = {"objective": "binary", "metric": "auc", "verbose": -1, "seed": self.seed,
                  "deterministic": True, "force_row_wise": True, "num_threads": self.threads, "bagging_freq": 1, **p}
        dtrain = _dataset(X, y, w)
        dval = _dataset(X_val, y_val, None, reference=dtrain)
        hist: dict = {}
        self.model = lgb.train(params, dtrain, num_boost_round=rounds, valid_sets=[dval], valid_names=["validation"],
                               callbacks=[lgb.early_stopping(patience, verbose=False), lgb.record_evaluation(hist)])
        return {"best_iteration": int(self.model.best_iteration), "validation_auc": hist["validation"]["auc"]}

    def predict_proba(self, X):
        return self.model.predict(X, num_iteration=self.model.best_iteration, num_threads=self.threads if self.threads > 0 else 0)

    def n_parameters(self):
        info = self.model.dump_model(num_iteration=self.model.best_iteration)["tree_info"]
        return int(sum(2 * t["num_leaves"] - 1 for t in info))

    def _save(self, path: Path):
        self.model.save_model(str(path / "model.txt"), num_iteration=self.model.best_iteration)

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"]); m.model = lgb.Booster(model_file=str(path / "model.txt")); return m
