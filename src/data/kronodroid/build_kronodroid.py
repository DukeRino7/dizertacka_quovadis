r"""V4 (docs/19): príprava KronoDroid v rovnakom formáte ako Quo Vadis (processed/static, processed/dynamic/tabular).

Pre každú vetvu vznikne priečinok `processed/kronodroid/<vetva>/` s podpriečinkami, ktoré čítajú spoločné moduly
(`src/data/providers.py` cez `DIZERTACKA_DATASET=<vetva>`):
    index/samples.parquet                       sha256, family, label, split, feature_group (+ údaje pre podskupiny)
    static/            X_*.npy, y_*.npy, meta_*.parquet, feature_names.csv, manifest.json
    dynamic/tabular/   to isté pre systémové volania
    dynamic/tabular_norm/   kontrolný experiment D-norm (podiely volaní, bez nr_syscalls)

Vetvy: real_full (celé skutočné zariadenie), real_p a emu_p (prekrytie, rovnaké súbory a rozdelenie),
real_time (doplnkový časový posun malvéru). Rozdelenie sa urobí raz na real_full; real_p a emu_p sú jeho podmnožina.
Spoločný index všetkých súborov: processed/kronodroid/index/samples.parquet (verzuje sa).

    .venv\Scripts\python.exe -m src.data.kronodroid.build_kronodroid
"""
import argparse
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.common.config import load_config
from src.common.paths import PROCESSED_DIR, rel
from src.common.provenance import describe_files, environment, git_info, now_iso, write_json
from .audit_kronodroid import column_groups, load_subset, md_table

SPLITS = ["train", "validation", "test"]
BRANCHES = ["real_full", "real_p", "emu_p", "real_time"]


def fold_assign(y_strat: np.ndarray, groups: np.ndarray, n_splits: int, seed: int) -> np.ndarray:
    """Číslo časti (0..n_splits-1) pre každý riadok; skupiny spolu, stratifikácia podľa y_strat."""
    fold = np.full(len(y_strat), -1)
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    for k, (_, idx) in enumerate(sgkf.split(np.zeros(len(y_strat)), y_strat, groups)):
        fold[idx] = k
    assert (fold >= 0).all()
    return fold


def main(config_path: str) -> None:
    t0 = time.perf_counter()
    cfg = load_config(config_path)
    b = cfg["build"]
    out_root = PROCESSED_DIR / "kronodroid"
    lab, famcol = cfg["columns"]["label"], cfg["columns"]["family"]

    R = load_subset(cfg, "real_device")
    E = load_subset(cfg, "emulator")
    g = column_groups(R, cfg)
    assert g["dynamic"] == column_groups(E, cfg)["dynamic"]
    perm = g["permissions"]
    meta_cols = [c for c in g["static_metadata"] if c not in b["drop_static"]]
    dyn = g["dynamic"]

    # 1) vyradenie SHA-256 s oboma označeniami (docs/18, bod 2) a jeden riadok na súbor
    bad = sorted(set(R.loc[R["sha"].duplicated(), "sha"]) | set(E.loc[E["sha"].duplicated(), "sha"]))
    R = R[~R["sha"].isin(bad)].set_index("sha")
    E = E[~E["sha"].isin(bad)].set_index("sha")
    overlap = R.index.intersection(E.index)
    assert (R.loc[overlap, lab] == E.loc[overlap, lab]).all()
    assert (R.loc[overlap, perm].values == E.loc[overlap, perm].values).all()

    # 2) statické metadáta: zo zariadenia, chýbajúce doplniť z emulátora (podľa SHA-256)
    meta_static = R[meta_cols].copy()
    fill = meta_static.loc[overlap].isna() & E.loc[overlap, meta_cols].notna()
    meta_static.loc[overlap] = meta_static.loc[overlap].mask(fill, E.loc[overlap, meta_cols])
    missing_meta = meta_static.isna().any(axis=1)
    # zvyšné chýbajúce metadáta = 0 + príznak meta_missing (rovnaký vstup pre všetky modely; StaticPreprocessor NaN nepozná)
    static = pd.concat([R[perm].astype(np.float32), meta_static.fillna(0).astype(np.float32),
                        missing_meta.astype(np.float32).rename("meta_missing")], axis=1)
    static_groups = (["permissions"] * len(perm) + ["metadata"] * len(meta_cols) + ["metadata"])

    # 3) rodiny: malvér = MalFamily (rodiny < min_family -> 'other', chýbajúca -> 'unknown'), neškodné = 'benign'
    fam = R[famcol].fillna("unknown").where(R[lab] == 1, "benign")
    counts = fam[R[lab] == 1].value_counts()
    rare = counts.index[counts < b["min_family"]]
    fam = fam.where(~fam.isin(rare), "other")

    # 4) skupiny identických statických vektorov (spolu v jednej časti, ako vo V1)
    feature_group = pd.Series(pd.util.hash_pandas_object(static.fillna(-1), index=False).values, index=static.index)
    feature_group = pd.factorize(feature_group)[0]

    # 5) hlavné rozdelenie 70/10/20 na celom zariadení (stratifikácia podľa triedy a rodiny)
    n_parts = b["n_parts"]   # 10 častí: 7 train, 1 validation, 2 test
    fold = fold_assign(fam.to_numpy(), feature_group, n_parts, b["seed"])
    split = np.select([fold < b["train_parts"], fold < b["train_parts"] + b["val_parts"]], ["train", "validation"], "test")

    year = R["date_last_dt"].dt.year
    idx = pd.DataFrame({
        "sha256": R.index, "family": fam.values, "label": R[lab].astype(int).values, "split": split,
        "feature_group": feature_group, "in_overlap": R.index.isin(overlap),
        "raw_family": R[famcol].values, "detection_ratio": R["Detection_Ratio"].values,
        "year": year.where(year.between(2008, 2020)).astype("Int64").values,
        "nr_syscalls_zero_real": (R["nr_syscalls"] == 0).values,
        "nr_syscalls_zero_emu": E["nr_syscalls"].reindex(R.index).eq(0).values,
        "meta_missing": missing_meta.values,
    })

    # 6) doplnkový časový posun malvéru: malvér 2008–2014 -> train/validation, 2015–2020 -> test,
    #    neplatný rok -> vynechaný; neškodné podľa hlavného rozdelenia. Skupina, ktorej člen ide do testu, ide celá do testu.
    t_split = idx["split"].copy()
    mal = idx["label"] == 1
    late = mal & idx["year"].ge(b["time_test_from"]).fillna(False)
    invalid = mal & idx["year"].isna()
    test_groups = set(idx.loc[late, "feature_group"])
    early = mal & ~late & ~invalid
    tv = fold_assign(idx.loc[early, "family"].to_numpy(), idx.loc[early, "feature_group"].to_numpy(), 8, b["seed"])
    t_split.loc[early] = np.where(tv < 7, "train", "validation")
    t_split.loc[late] = "test"
    t_split.loc[idx["feature_group"].isin(test_groups)] = "test"
    t_split.loc[invalid] = "excluded"
    idx["split_time"] = t_split.values

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "index").mkdir(exist_ok=True)
    idx.to_parquet(out_root / "index" / "samples.parquet", index=False)

    branches = {
        "real_full": (idx, "split", R),
        "real_p": (idx[idx["in_overlap"]], "split", R),
        "emu_p": (idx[idx["in_overlap"]], "split", E),
        "real_time": (idx[idx["split_time"] != "excluded"], "split_time", R),
    }
    report = {}
    for name, (I, scol, D) in branches.items():
        base = out_root / name
        sub = I.assign(split=I[scol])[["sha256", "family", "label", "split", "feature_group"]]
        (base / "index").mkdir(parents=True, exist_ok=True)
        sub.to_parquet(base / "index" / "samples.parquet", index=False)
        Xd = D.loc[sub["sha256"], dyn].to_numpy(np.float64)
        total = Xd[:, -1:]
        Xn = np.divide(Xd[:, :-1], total, out=np.zeros_like(Xd[:, :-1]), where=total > 0)
        reps = {"static": (static.loc[sub["sha256"]].to_numpy(np.float32), static.columns.tolist(), static_groups),
                "dynamic/tabular": (Xd.astype(np.float32), dyn, ["syscalls"] * (len(dyn) - 1) + ["total"]),
                "dynamic/tabular_norm": (Xn.astype(np.float32), [f"{c}_share" for c in dyn[:-1]], ["syscalls"] * (len(dyn) - 1))}
        report[name] = {"n": len(sub), "by_split": sub.groupby("split")["label"].agg(["size", "sum"]).to_dict("index")}
        for rep, (X, names, groups) in reps.items():
            d = base / rep
            d.mkdir(parents=True, exist_ok=True)
            files = []
            for s in SPLITS:
                m = (sub["split"] == s).to_numpy()
                np.save(d / f"X_{s}.npy", X[m]); np.save(d / f"y_{s}.npy", sub["label"].to_numpy(np.int8)[m])
                meta = sub.loc[m, ["sha256", "family", "label"] + (["feature_group"] if rep == "static" else [])]
                meta.reset_index(drop=True).to_parquet(d / f"meta_{s}.parquet", index=False)
                files += [d / f"X_{s}.npy", d / f"y_{s}.npy", d / f"meta_{s}.parquet"]
            pd.DataFrame({"column": range(len(names)), "group": groups, "name": names}).to_csv(d / "feature_names.csv", index=False)
            write_json({"script": "src/data/kronodroid/build_kronodroid.py", "created": now_iso(), "branch": name,
                        "representation": rep, "n_features": len(names), "config": cfg, "git": git_info(),
                        "outputs": describe_files(files)}, d / "manifest.json")
        print(f"{name}: {len(sub)} súborov", report[name]["by_split"], flush=True)

    # súhrn (verzuje sa)
    def tbl(I, scol):
        return md_table(pd.crosstab(I[scol], I["label"].map({0: "benign", 1: "malware"})))

    hold = cfg["v4"]["holdout_families"]
    fam_tbl = "\n".join(f"| {f} | {int((idx['family'] == f).sum())} | {int(((idx['family'] == f) & idx['in_overlap']).sum())} |"
                        for f in hold)
    text = f"""# KronoDroid – pripravené dáta (V4)

> Generované `src/data/kronodroid/build_kronodroid.py` ({now_iso()}). Plán: `docs/19_plan_v4.md`.

- vyradené SHA-256 s oboma označeniami: {len(bad)}; súbory zariadenia: {len(R)}, prekrytie s emulátorom: {len(overlap)}
- statika: {len(perm)} oprávnení + {len(meta_cols)} metadát (bez {b['drop_static']}) + meta_missing = {static.shape[1]} príznakov;
  metadáta doplnené z emulátora v {int(fill.any(axis=1).sum())} súboroch, stále chýbajú v {int(missing_meta.sum())}
- dynamika: {len(dyn)} stĺpcov (systémové volania + nr_syscalls); D-norm: {len(dyn) - 1} podielov
- rodiny malvéru s < {b['min_family']} vzorkami -> 'other' ({len(rare)} rodín), bez rodiny -> 'unknown'
- skupiny identických statických vektorov: {int(feature_group.max()) + 1}

## Hlavné rozdelenie (real_full; real_p a emu_p sú jeho podmnožina)
{tbl(idx, 'split')}

### Prekrytie (real_p, emu_p)
{tbl(idx[idx['in_overlap']], 'split')}

## Doplnkový časový posun malvéru (real_time): test = malvér od roku {b['time_test_from']}
{tbl(idx, 'split_time')}

## Vynechávané rodiny (zero-day)
| rodina | real_full | prekrytie |
|---|---|---|
{fam_tbl}
"""
    (out_root / "README.md").write_text(text, encoding="utf-8")
    write_json({"script": "src/data/kronodroid/build_kronodroid.py", "created": now_iso(), "config": cfg,
                "removed_sha256": bad, "branches": report, "duration_s": round(time.perf_counter() - t0, 1),
                "git": git_info(), "environment": environment(),
                "outputs": describe_files([out_root / "index" / "samples.parquet", out_root / "README.md"])},
               out_root / "manifest.json")
    print(f"hotovo za {time.perf_counter() - t0:.0f} s -> {rel(out_root)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/kronodroid/data.yaml")
    main(ap.parse_args().config)
