"""Učené transformácie EMBER príznakov pre modely, ktoré ich potrebujú (napr. LR, neurónové siete).

Transformácie sa NEaplikujú na uložený dataset v processed/static (ten obsahuje pôvodné hodnoty).
Fitujú sa iba na tréningovej časti vo vnútri konkrétneho experimentu a ukladajú sa s modelom do runs/.
Stromové modely (napr. LightGBM, XGBoost) ich spravidla nepotrebujú.
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def signed_log1p(X: np.ndarray) -> np.ndarray:
    """sign(x) * log(1 + |x|): stlačí ťažké chvosty (veľkosti súborov, adresy) a zachová znamienko
    (hašované bloky EMBER obsahujú záporné hodnoty)."""
    return np.sign(X) * np.log1p(np.abs(X))


class StaticPreprocessor(BaseEstimator, TransformerMixin):
    """Voliteľne: odstránenie konštantných stĺpcov -> signed log1p -> štandardizácia.

    Všetky parametre (zoznam stĺpcov, priemery, smerodajné odchýlky) sa učia výhradne vo `fit`
    na dátach, ktoré dostane – v experimentoch je to tréningová časť.
    """

    def __init__(self, drop_constant: bool = True, log_transform: bool = True,
                 standardize: bool = True, clip: float | None = None, dtype=np.float32):
        self.drop_constant = drop_constant
        self.log_transform = log_transform
        self.standardize = standardize
        self.clip = clip
        self.dtype = dtype

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=np.float64)
        n = X.shape[1]
        self.keep_ = (X.max(axis=0) != X.min(axis=0)) if self.drop_constant else np.ones(n, bool)
        Z = signed_log1p(X[:, self.keep_]) if self.log_transform else X[:, self.keep_]
        self.mean_ = Z.mean(axis=0) if self.standardize else np.zeros(Z.shape[1])
        std = Z.std(axis=0) if self.standardize else np.ones(Z.shape[1])
        self.scale_ = np.where(std > 0, std, 1.0)
        self.n_features_in_ = n
        return self

    def transform(self, X):
        X = np.asarray(X)[:, self.keep_].astype(np.float64, copy=False)
        if self.log_transform:
            X = signed_log1p(X)
        X = (X - self.mean_) / self.scale_
        if self.clip is not None:
            X = np.clip(X, -self.clip, self.clip)
        return X.astype(self.dtype)
