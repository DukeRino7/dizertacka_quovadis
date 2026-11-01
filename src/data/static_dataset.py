"""Načítanie predspracovaného statického datasetu z processed/static (pre modely)."""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.common.paths import STATIC_DIR

SPLITS = ("train", "validation", "test")


@dataclass
class StaticSplit:
    X: np.ndarray          # [n, 2381] float32, pôvodné EMBER hodnoty
    y: np.ndarray          # [n] int8, 0 = benign, 1 = malware
    meta: pd.DataFrame     # sha256, family, label, feature_group (riadky zarovnané s X)


def load_split(split: str, mmap: bool = True) -> StaticSplit:
    if split not in SPLITS:
        raise ValueError(f"neznáma časť {split!r}, povolené: {SPLITS}")
    X = np.load(STATIC_DIR / f"X_{split}.npy", mmap_mode="r" if mmap else None)
    y = np.load(STATIC_DIR / f"y_{split}.npy")
    meta = pd.read_parquet(STATIC_DIR / f"meta_{split}.parquet")
    assert len(X) == len(y) == len(meta)
    return StaticSplit(X, y, meta)


def feature_names() -> pd.DataFrame:
    return pd.read_csv(STATIC_DIR / "feature_names.csv")
