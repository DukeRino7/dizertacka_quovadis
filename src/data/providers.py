"""Jednotný prístup k dátam pre modely podľa prístupu (modality).

Vracia slovník časť -> (X, y, meta). Rozdelenie je vždy to spoločné z processed/index.
"""
import numpy as np
import pandas as pd


def load_tabular(approach: str, splits=("train", "validation", "test")) -> dict[str, tuple[np.ndarray, np.ndarray, pd.DataFrame]]:
    if approach == "static":
        from .static_dataset import load_split
        out = {}
        for s in splits:
            d = load_split(s, mmap=False)
            out[s] = (d.X, d.y, d.meta)
        return out
    if approach in ("dynamic", "hybrid"):
        raise NotImplementedError(f"dáta pre {approach!r} ešte nie sú pripravené (čaká sa na Speakeasy)")
    raise ValueError(approach)
