"""Jednotný prístup k dátam pre modely podľa prístupu (modality).

Vracia slovník časť -> (X, y, meta). Rozdelenie je vždy to spoločné z processed/index;
poradie riadkov je vo všetkých prístupoch rovnaké (overuje sa podľa SHA-256).

- static  : processed/static            (EMBER, 2381 príznakov)
- dynamic : processed/dynamic/tabular   (n-gramy API, udalosti, súhrn reportu)
- hybrid  : spojenie static | dynamic   (ranná fúzia – jeden vektor)
- dynamic_seq : processed/dynamic/sequence (ID tokenov API, int32 [n, max_len]) – sekvenčné modely
- hybrid_seq  : static | ID tokenov (float32) – dvojvetvová sieť, model si vstup rozdelí podľa n_static
"""
import numpy as np
import pandas as pd

from src.common.paths import PROCESSED_DIR, STATIC_DIR

DIRS = {"static": STATIC_DIR, "dynamic": PROCESSED_DIR / "dynamic" / "tabular",
        "dynamic_seq": PROCESSED_DIR / "dynamic" / "sequence"}


def _load_dir(base, split: str):
    X = np.load(base / f"X_{split}.npy")
    y = np.load(base / f"y_{split}.npy")
    meta = pd.read_parquet(base / f"meta_{split}.parquet")
    assert len(X) == len(y) == len(meta)
    return X, y, meta


def load_tabular(approach: str, splits=("train", "validation", "test")) -> dict[str, tuple[np.ndarray, np.ndarray, pd.DataFrame]]:
    out = {}
    for s in splits:
        if approach in DIRS:
            out[s] = _load_dir(DIRS[approach], s)
        elif approach in ("hybrid", "hybrid_seq"):
            Xs, ys, ms = _load_dir(DIRS["static"], s)
            Xd, yd, md = _load_dir(DIRS["dynamic" if approach == "hybrid" else "dynamic_seq"], s)
            if not (ms["sha256"].to_numpy() == md["sha256"].to_numpy()).all() or not (ys == yd).all():
                raise ValueError(f"{s}: statické a dynamické dáta nie sú zarovnané podľa SHA-256")
            out[s] = (np.hstack([Xs, Xd.astype(np.float32)]), ys, ms)
        else:
            raise ValueError(approach)
    return out


def feature_table(approach: str) -> pd.DataFrame:
    """Tabuľka príznakov: name, group (pri hybride s predponou static:/dynamic: v skupine)."""
    if approach in DIRS:
        return pd.read_csv(DIRS[approach] / "feature_names.csv")[["name", "group"]]
    if approach == "hybrid":
        s = feature_table("static").assign(group=lambda d: "static:" + d["group"])
        d = feature_table("dynamic").assign(group=lambda d: "dynamic:" + d["group"])
        return pd.concat([s, d], ignore_index=True)
    raise ValueError(approach)


def feature_names(approach: str) -> list[str]:
    return feature_table(approach)["name"].tolist()
