"""Spoločný index vzoriek a rozdelenie train/validation/test.

Spustenie (z koreňa projektu):
    .venv\\Scripts\\python.exe -m src.data.build_index --config configs/data/index.yaml

Výstup v processed/index/:
    samples.parquet       jedna použitá vzorka na riadok (sha256, family, label, original_split, split, ...)
    excluded.parquet      vyradené vzorky a dôvod
    ember_errors.parquet  súbory, pri ktorých zlyhala extrakcia EMBER (v datasete chýbajú príznaky)
    manifest.json         konfigurácia, verzia kódu, kontrolné súčty vstupov aj výstupov
    README.md             automaticky generovaný popis a počty
"""
import argparse
import hashlib
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.common.config import load_config
from src.common.paths import INDEX_DIR, PROJECT_ROOT, rel, resolve
from src.common.provenance import describe_files, environment, git_info, now_iso, write_json
from .ember_source import read_catalog
from .speakeasy_listing import read_listing

SPLIT_ORDER = ["train", "validation", "test"]


def feature_hashes(catalog: pd.DataFrame) -> np.ndarray:
    """MD5 bajtov každého EMBER vektora (na odhalenie identických vektorov pri rôznych SHA-256)."""
    out = np.empty(len(catalog), dtype=object)
    for file, part in catalog.groupby("ember_file", sort=False):
        X = np.load(PROJECT_ROOT / file, mmap_mode="r")
        for pos, row in zip(part.index.to_numpy(), part["ember_row"].to_numpy()):
            out[pos] = hashlib.md5(np.ascontiguousarray(X[row]).tobytes()).hexdigest()
    return out


def handle_cross_split(cat: pd.DataFrame, policy: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    dup = cat["sha256"].duplicated(keep=False)
    if policy == "keep":
        return cat, cat.iloc[0:0].assign(reason=[])
    drop_split = {"drop_from_train": "train", "drop_from_test": "test"}[policy]
    mask = dup & (cat["original_split"] == drop_split)
    excluded = cat[mask].assign(reason=f"SHA-256 aj v druhej časti pôvodného rozdelenia ({policy})")
    return cat[~mask].reset_index(drop=True), excluded


def assign_validation(df: pd.DataFrame, cfg: dict, seed: int) -> pd.Series:
    split = df["original_split"].copy()
    train_pos = np.flatnonzero(df["original_split"].to_numpy() == "train")
    tr = df.iloc[train_pos]
    n_splits = int(round(1 / cfg["fraction"]))
    groups = tr["feature_group"] if cfg.get("group_identical_features", True) else np.arange(len(tr))
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    _, val_idx = next(sgkf.split(np.zeros(len(tr)), tr[cfg["stratify_by"]], groups))
    split.iloc[train_pos[val_idx]] = "validation"
    return split


def counts_table(df: pd.DataFrame) -> pd.DataFrame:
    t = df.pivot_table(index="family", columns="split", values="sha256", aggfunc="count", fill_value=0)
    t = t.reindex(columns=[c for c in SPLIT_ORDER if c in t.columns])
    fams = ["benign"] + sorted(f for f in t.index if f != "benign")
    t = t.reindex(fams)
    t.loc["SPOLU"] = t.sum()
    return t


def md_table(df: pd.DataFrame, index_name: str = "") -> str:
    cols = [index_name] + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for idx, row in df.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [f"{v:,}".replace(",", " ") if isinstance(v, (int, np.integer)) else str(v) for v in row]) + " |")
    return "\n".join(lines)


def write_readme(df, excluded, errors, cfg, manifest, path):
    t = counts_table(df)
    lab = df.pivot_table(index="split", columns="label", values="sha256", aggfunc="count").reindex(SPLIT_ORDER)
    lab.columns = ["benign (0)", "malware (1)"]
    lab["podiel malware"] = (lab["malware (1)"] / lab.sum(axis=1)).map(lambda v: f"{v:.3f}")
    val = cfg["validation"]
    text = f"""# processed/index/ – spoločný index vzoriek a rozdelenie

> Automaticky generované skriptom `src/data/build_index.py` ({manifest['created']}).
> Konfigurácia: `{manifest['config_path']}`. Neupravovať ručne – pri zmene spustiť skript znova.

Tento index a rozdelenie používajú **všetky** modely (statické, dynamické, hybridné, študenti, kaskáda).
Vzorka = jeden PE súbor identifikovaný SHA-256.

## Súbory
| Súbor | Obsah |
|---|---|
| `samples.parquet` | použité vzorky: `sha256`, `family`, `label` (0 benign / 1 malware), `original_split`, `split`, `feature_group`, `ember_file`, `ember_row`, `speakeasy_path`, `speakeasy_bytes` |
| `excluded.parquet` | vyradené vzorky s dôvodom |
| `ember_errors.parquet` | súbory bez EMBER príznakov (zlyhaná extrakcia v pôvodnom datasete) |
| `manifest.json` | konfigurácia, commit, prostredie, kontrolné súčty vstupov a výstupov |

## Postup
1. Načítanie katalógu EMBER s kontrolou integrity (indexy, nulové riadky zlyhaných extrakcií, platnosť SHA-256).
   Riadok matice sa určuje indexom z `hashes.txt`.
2. Vynechanie {len(errors)} súborov so zlyhanou extrakciou EMBER (príznaky neexistujú).
3. Prekryv pôvodného train/test podľa SHA-256: politika `{cfg['cross_split_duplicates']}`,
   vyradených {len(excluded)} záznamov.
4. Zoskupenie vzoriek s identickým EMBER vektorom (MD5 bajtov vektora → `feature_group`).
5. Vyčlenenie validácie z pôvodného tréningu: `StratifiedGroupKFold`, {int(round(1/val['fraction']))} častí,
   jedna časť = validácia (podiel {val['fraction']}), stratifikácia podľa `{val['stratify_by']}`,
   skupiny identických vektorov {'vždy spolu' if val.get('group_identical_features', True) else 'nezohľadnené'}, seed {cfg['seed']}.
   Pôvodný test zostáva bez zmeny (časový posun: tréning január 2022, test apríl 2022).
6. Priradenie Speakeasy reportu podľa SHA-256 (zo zoznamu súborov na Hugging Face).

## Počty podľa rodiny a časti
{md_table(t, 'rodina')}

## Binárne označenie
{md_table(lab, 'časť')}

## Kontroly
- Unikátne SHA-256 v indexe: {df['sha256'].is_unique}
- Vzorky so Speakeasy reportom v zozname súborov: {int(df['speakeasy_path'].notna().sum())} z {len(df)}
- Zhoda rodiny EMBER vs. Speakeasy priečinok: {int((df['family'] == df['speakeasy_family']).sum())} z {int(df['speakeasy_path'].notna().sum())}
- Skupiny identických EMBER vektorov s viac ako 1 vzorkou: {int((df['feature_group'].value_counts() > 1).sum())}
  (vzoriek v nich: {int(df['feature_group'].map(df['feature_group'].value_counts()).gt(1).sum())});
  skupiny cez viac častí rozdelenia: {int(df.groupby('feature_group')['split'].nunique().gt(1).sum())};
  skupiny s rozporným označením: {int(df.groupby('feature_group')['label'].nunique().gt(1).sum())}

## Rozhodnutia označené ako NÁVRH (neschválené)
- veľkosť validácie ({val['fraction']}),
- politika prekryvu train/test (`{cfg['cross_split_duplicates']}`).
Zmena = úprava `{manifest['config_path']}` a nové spustenie skriptu.
"""
    path.write_text(text, encoding="utf-8")


def main(config_path: str) -> None:
    t0 = time.perf_counter()
    cfg = load_config(config_path)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    cat, errors = read_catalog()
    if cat.duplicated(["sha256", "original_split"]).any():
        raise ValueError("Duplicitné SHA-256 v rámci jednej časti – audit to nepredpokladal, treba preveriť.")
    n_raw = len(cat)

    cat, excluded = handle_cross_split(cat, cfg["cross_split_duplicates"])
    cat["feature_group"] = pd.Series(feature_hashes(cat)).factorize()[0]

    listing = read_listing(resolve(cfg["speakeasy_listing"]))
    listing = listing.rename(columns={"family": "speakeasy_family"})
    cat = cat.merge(listing, on=["sha256", "original_split"], how="left", validate="one_to_one")

    cat["split"] = assign_validation(cat, cfg["validation"], cfg["seed"])
    cat = cat.sort_values(["split", "family", "sha256"], key=lambda s: s.map({k: i for i, k in enumerate(SPLIT_ORDER)}) if s.name == "split" else s).reset_index(drop=True)

    cols = ["sha256", "family", "label", "original_split", "split", "feature_group",
            "ember_file", "ember_row", "speakeasy_path", "speakeasy_bytes", "speakeasy_family"]
    out_files = {
        "samples": INDEX_DIR / "samples.parquet",
        "excluded": INDEX_DIR / "excluded.parquet",
        "ember_errors": INDEX_DIR / "ember_errors.parquet",
    }
    cat[cols].to_parquet(out_files["samples"], index=False)
    excluded.to_parquet(out_files["excluded"], index=False)
    errors.to_parquet(out_files["ember_errors"], index=False)

    manifest = {
        "created": now_iso(),
        "script": "src/data/build_index.py",
        "config_path": rel(resolve(config_path)),
        "config": cfg,
        "git": git_info(),
        "environment": environment(),
        "inputs": describe_files(sorted(resolve("data/quovadis-ember").glob("*/*/hashes.txt"))),
        "counts": {"ember_ok_rows": n_raw, "excluded": len(excluded), "samples": len(cat),
                   "per_split": cat["split"].value_counts().reindex(SPLIT_ORDER).to_dict()},
        "duration_s": None,
    }
    write_readme(cat, excluded, errors, cfg, manifest, INDEX_DIR / "README.md")
    manifest["outputs"] = describe_files(list(out_files.values()))
    manifest["duration_s"] = round(time.perf_counter() - t0, 1)
    write_json(manifest, INDEX_DIR / "manifest.json")
    print(f"Index hotový: {len(cat)} vzoriek, {manifest['counts']['per_split']}, {manifest['duration_s']} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/data/index.yaml")
    main(ap.parse_args().config)
