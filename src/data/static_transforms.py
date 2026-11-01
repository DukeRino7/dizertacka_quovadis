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
        # Výpočet vo float32 a na mieste (in-place): rovnaký vzorec ako predtým, ale bez zbytočných kópií
        # vo float64 – inak úprava vstupu zbytočne nafukuje nameraný čas a pamäť LR a MLP pri inferencii.
        if not hasattr(self, "_mean32"):
            self._mean32 = self.mean_.astype(np.float32)
            self._inv_scale32 = (1.0 / self.scale_).astype(np.float32)
        Z = np.asarray(X, dtype=np.float32)[:, self.keep_]   # výber stĺpcov vytvorí novú kópiu
        if self.log_transform:
            A = np.abs(Z)
            np.log1p(A, out=A)
            np.copysign(A, Z, out=A)                         # sign(x) * log(1 + |x|)
            Z = A
        Z -= self._mean32
        Z *= self._inv_scale32
        if self.clip is not None:
            np.clip(Z, -self.clip, self.clip, out=Z)
        return Z if self.dtype == np.float32 else Z.astype(self.dtype)
