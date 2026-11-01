"""Čítanie pôvodných EMBER súborov z data/quovadis-ember (iba čítanie, nič sa nemení).

Formát (overený v audite, docs/01_audit_dat.md):
    {train,test}/<rodina>/features.npy   float32 [N, 2381], N = úspešné + zlyhané
    {train,test}/<rodina>/hashes.txt     riadky "index,sha256" úspešných vzoriek
    {train,test}/<rodina>/errors.log     riadky "index,sha256,chyba" zlyhaných vzoriek
Riadok vzorky v matici určuje index z hashes.txt (nie poradie riadku v hashes.txt).
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.paths import EMBER_DIR, PROJECT_ROOT, rel
from .ember_layout import EMBER_DIM

SPLITS = ("train", "test")
BENIGN = "benign"
_SHA = re.compile(r"^[0-9a-f]{64}$")


def _read_lines(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def read_catalog(root: Path = EMBER_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Vráti (vzorky, chyby). Vzorky: sha256, family, label, original_split, ember_file, ember_row.

    Pri čítaní overuje integritu a pri porušení vyhodí výnimku:
    tvar a typ matice, platnosť SHA-256, rozsah indexov, nenulovosť riadkov úspešných vzoriek
    a nulovosť riadkov zlyhaných vzoriek.
    """
    samples, errors = [], []
    for split in SPLITS:
        for fam_dir in sorted(p for p in (root / split).iterdir() if p.is_dir()):
            family = fam_dir.name
            feat = fam_dir / "features.npy"
            X = np.load(feat, mmap_mode="r")
            if X.ndim != 2 or X.shape[1] != EMBER_DIM or X.dtype != np.float32:
                raise ValueError(f"{feat}: neočakávaný tvar/typ {X.shape} {X.dtype}")

            ok = [line.split(",", 1) for line in _read_lines(fam_dir / "hashes.txt")]
            bad = [line.split(",", 2) for line in _read_lines(fam_dir / "errors.log")]
            ok_idx = np.array([int(i) for i, _ in ok])
            bad_idx = np.array([int(e[0]) for e in bad], dtype=int)

            if len(ok_idx) + len(bad_idx) != X.shape[0]:
                raise ValueError(f"{fam_dir}: úspešné + zlyhané != počet riadkov matice")
            if len(np.unique(np.concatenate([ok_idx, bad_idx]))) != X.shape[0]:
                raise ValueError(f"{fam_dir}: indexy sa prekrývajú alebo chýbajú")
            if not np.all(np.abs(np.asarray(X[np.sort(ok_idx)])).sum(axis=1) > 0):
                raise ValueError(f"{fam_dir}: nulový riadok pri úspešnej vzorke")
            if len(bad_idx) and np.any(np.asarray(X[np.sort(bad_idx)]) != 0):
                raise ValueError(f"{fam_dir}: nenulový riadok pri zlyhanej vzorke")

            for (i, sha) in ok:
                if not _SHA.match(sha):
                    raise ValueError(f"{fam_dir}: neplatné SHA-256 {sha!r}")
                samples.append((sha, family, int(family != BENIGN), split, rel(feat), int(i)))
            for e in bad:
                errors.append((e[1], family, split, int(e[0]), e[2] if len(e) > 2 else ""))

    s = pd.DataFrame(samples, columns=["sha256", "family", "label", "original_split", "ember_file", "ember_row"])
    e = pd.DataFrame(errors, columns=["sha256", "family", "original_split", "ember_row", "error"])
    return s, e


def load_rows(catalog: pd.DataFrame, dtype=np.float32) -> np.ndarray:
    """Načíta príznaky pre riadky katalógu v ich poradí (podľa ember_file a ember_row)."""
    catalog = catalog.reset_index(drop=True)
    out = np.empty((len(catalog), EMBER_DIM), dtype=dtype)
    for file, part in catalog.groupby("ember_file", sort=False):
        X = np.load(PROJECT_ROOT / file, mmap_mode="r")
        rows = part["ember_row"].to_numpy()
        order = np.argsort(rows)  # sekvenčné čítanie z mmap
        out[part.index.to_numpy()[order]] = np.asarray(X[rows[order]], dtype=dtype)
    return out
