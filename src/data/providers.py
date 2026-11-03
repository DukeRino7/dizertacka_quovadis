"""Jednotný prístup k dátam pre modely podľa prístupu (modality).

Vracia slovník časť -> (X, y, meta). Rozdelenie je vždy to spoločné z processed/index;
poradie riadkov je vo všetkých prístupoch rovnaké (overuje sa podľa SHA-256).

- static  : processed/static            (EMBER, 2381 príznakov)
- dynamic : processed/dynamic/tabular   (n-gramy API, udalosti, súhrn reportu)
- hybrid  : spojenie static | dynamic   (ranná fúzia – jeden vektor)
- dynamic_seq : processed/dynamic/sequence (ID tokenov API, int32 [n, max_len]) – sekvenčné modely
- hybrid_seq  : static | ID tokenov (float32) – dvojvetvová sieť, model si vstup rozdelí podľa n_static

Zero-day (docs/09, premenná DIZERTACKA_HOLDOUT_FAMILY): rodina sa odstráni z train aj validation, dynamické
reprezentácie sa berú zo slovníka bez nej (processed/dynamic/lofo/<rodina>/) a jej vzorky z train + validation
sú dostupné ako časť 'holdout' (iba malvér; nevidené modelom). Test ostáva celý.
"""
import numpy as np
import pandas as pd

from src.common import paths
from src.common.paths import PROCESSED_DIR, STATIC_DIR

DIRS = {"static": STATIC_DIR, "dynamic": PROCESSED_DIR / "dynamic" / "tabular",
        "dynamic_seq": PROCESSED_DIR / "dynamic" / "sequence",
        "dynamic_full": PROCESSED_DIR / "dynamic" / "tabular_full"}   # kontrolný variant s udalosťami a súhrnom


def _load_dir(base, split: str):
    X = np.load(base / f"X_{split}.npy")
    y = np.load(base / f"y_{split}.npy")
    meta = pd.read_parquet(base / f"meta_{split}.parquet")
    assert len(X) == len(y) == len(meta)
    return X, y, meta


def _dirs() -> dict:
    """Priečinky dát; pri zero-day behu dynamické reprezentácie bez vynechanej rodiny."""
    fam = paths.HOLDOUT_FAMILY
    if not fam:
        return DIRS
    lofo = PROCESSED_DIR / "dynamic" / "lofo" / fam
    for sub in ("tabular", "sequence"):
        if not (lofo / sub / "manifest.json").exists():
            raise FileNotFoundError(f"chýba {lofo / sub} – spustiť build_dynamic_tabular/_sequence --exclude-family {fam}")
    return {**DIRS, "dynamic": lofo / "tabular", "dynamic_seq": lofo / "sequence"}


def load_tabular(approach: str, splits=("train", "validation", "test")) -> dict[str, tuple[np.ndarray, np.ndarray, pd.DataFrame]]:
    fam = paths.HOLDOUT_FAMILY
    if not fam:
        return _load_splits(approach, splits, DIRS)
    if "holdout" in splits:
        raise ValueError("časť 'holdout' sa nežiada priamo – vznikne automaticky pri zero-day behu")
    need = sorted(set(splits) | {"train", "validation"}, key=["train", "validation", "test"].index)
    raw = _load_splits(approach, need, _dirs())
    out, held = {}, []
    for s in need:
        X, y, m = raw.pop(s)   # pop: pôvodné pole sa uvoľní hneď po výbere (nižšia špička pamäte)
        if s in ("train", "validation"):
            hold = (m["family"] == fam).to_numpy()
            if not hold.any():
                raise ValueError(f"rodina {fam!r} sa v časti {s} nenachádza")
            held.append((X[hold], y[hold], m[hold]))
            X, y, m = X[~hold], y[~hold], m[~hold].reset_index(drop=True)
        if s in splits:
            out[s] = (X, y, m)
    out["holdout"] = (np.vstack([h[0] for h in held]), np.concatenate([h[1] for h in held]),
                      pd.concat([h[2] for h in held], ignore_index=True))
    return out


def _load_splits(approach: str, splits, DIRS: dict) -> dict:
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
        return pd.read_csv(_dirs()[approach] / "feature_names.csv")[["name", "group"]]
    if approach == "hybrid":
        s = feature_table("static").assign(group=lambda d: "static:" + d["group"])
        d = feature_table("dynamic").assign(group=lambda d: "dynamic:" + d["group"])
        return pd.concat([s, d], ignore_index=True)
    raise ValueError(approach)


def feature_names(approach: str) -> list[str]:
    return feature_table(approach)["name"].tolist()
