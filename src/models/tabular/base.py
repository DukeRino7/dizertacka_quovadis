"""Spoločné rozhranie modelov rebríčka (rovnaké pre static, dynamic, hybrid)."""
import json
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class TabularModel(ABC):
    """Model nad pevným vektorom príznakov. Výstup predict_proba = P(malware)."""

    name: str = "base"
    needs_scaling: bool = False   # True -> pred modelom sa použije StaticPreprocessor (fit iba na tréningu)
    supports_gpu: bool = False

    def __init__(self, params: dict, seed: int, threads: int = -1):
        self.params = dict(params)
        self.seed = seed
        self.threads = threads

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray, w: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> dict:
        """Natrénuje model; validáciu smie použiť iba na early stopping. Vráti históriu učenia."""

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray: ...

    @abstractmethod
    def n_parameters(self) -> int:
        """Počet naučených parametrov (pri stromoch počet uzlov) – miera veľkosti modelu."""

    @abstractmethod
    def _save(self, path: Path) -> None: ...

    @classmethod
    @abstractmethod
    def _load(cls, path: Path, meta: dict) -> "TabularModel": ...

    def set_threads(self, n: int) -> None:
        self.threads = n

    def save(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "model_meta.json", "w", encoding="utf-8") as f:
            json.dump({"name": self.name, "params": self.params, "seed": self.seed, **self._extra_meta()}, f, indent=2)
        self._save(path)

    def _extra_meta(self) -> dict:
        return {}

    @classmethod
    def load(cls, path: Path) -> "TabularModel":
        with open(path / "model_meta.json", encoding="utf-8") as f:
            meta = json.load(f)
        return cls._load(path, meta)
