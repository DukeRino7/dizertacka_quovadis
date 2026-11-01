"""Dynamický dataset pre spoločný rebríček modelov -> processed/dynamic/tabular/.

Vstup: processed/dynamic/cache (src/data/build_dynamic.py). Slovník n-gramov sa učí IBA na tréningu
(ApiNgramVectorizer); je to spoločná reprezentácia pre všetky dynamické a hybridné modely rebríčka,
preto sa ukladá sem (s manifestom), nie do behu modelu.

    .venv\\Scripts\\python.exe -m src.data.build_dynamic_tabular
Výstup ako pri statických dátach: X_<časť>.npy, y_<časť>.npy, meta_<časť>.parquet, feature_names.csv,
vectorizer.joblib, train_feature_stats.parquet, drift_ks.parquet, plots/, STATISTICS.md, README.md, manifest.json.
"""
import argparse
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.common.config import load_config
from src.common.paths import INDEX_DIR, PROCESSED_DIR, rel
from src.common.provenance import describe_files, environment, git_info, now_iso, write_json
from src.evaluation import plots as P
from .build_static import column_stats, drift_table
from .dynamic_features import ApiNgramVectorizer

SPLIT_ORDER = ["train", "validation", "test"]


def main(cache: Path, out: Path, cfg_path: str, splits=SPLIT_ORDER, variant: str | None = None):
    t0 = time.perf_counter()
    cfg = load_config(cfg_path)
    tcfg = {**cfg["tabular"], **(cfg.get("tabular_variants", {}).get(variant, {}) if variant else {})}
    if variant and variant not in cfg.get("tabular_variants", {}):
        raise ValueError(f"neznámy variant {variant!r}")
    seed = load_config("configs/data/index.yaml")["seed"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "plots").mkdir(exist_ok=True)
    index = pd.read_parquet(INDEX_DIR / "samples.parquet")

    cols = ["sha256", "family", "label", "status", "api_seq", "events", "n_entry_points", "n_threads", "n_api_calls",
            "n_api_unique", "n_api_module_entry", "max_api_per_ep", "n_ep_errors", "n_events", "n_dynamic_code_segments"]
    data = {s: pd.read_parquet(cache / f"{s}.parquet", columns=cols) for s in splits}
    for s, d in data.items():  # poradie a úplnosť voči spoločnému indexu
        ref = index.loc[index["split"] == s, "sha256"].to_numpy()
        if len(d) != len(ref) or not (d["sha256"].to_numpy() == ref).all():
            raise ValueError(f"{s}: cache nezodpovedá indexu (chýbajúce vzorky alebo iné poradie) – "
                             f"spustiť build_dynamic na kompletných dátach")

    t = time.perf_counter()
    vec = ApiNgramVectorizer(**tcfg).fit(data["train"])
    fit_s = time.perf_counter() - t
    joblib.dump(vec, out / "vectorizer.joblib")
    feats = vec.feature_table()
    feats.to_csv(out / "feature_names.csv", index=False)

    X, sizes, outputs = {}, {}, []
    t = time.perf_counter()
    for s, d in data.items():
        Xs = vec.transform(d)
        np.save(out / f"X_{s}.npy", Xs)
        np.save(out / f"y_{s}.npy", d["label"].to_numpy(np.int8))
        d[["sha256", "family", "label"]].to_parquet(out / f"meta_{s}.parquet", index=False)
        outputs += [out / f"X_{s}.npy", out / f"y_{s}.npy", out / f"meta_{s}.parquet"]
        sizes[s] = Xs.nbytes / 1e6
        X[s] = Xs
    transform_s = time.perf_counter() - t

    stats = column_stats(X["train"]).merge(feats, on="column")
    stats.to_parquet(out / "train_feature_stats.parquet", index=False)
    drift = None
    if all(s in X for s in SPLIT_ORDER):
        drift = drift_table(X, {"max_rows_per_split": 20000}, seed).merge(feats, on="column")
        drift.to_parquet(out / "drift_ks.parquet", index=False)

    write_statistics(data, X, feats, stats, drift, vec, out)
    write_json({"created": now_iso(), "script": "src/data/build_dynamic_tabular.py", "config": tcfg,
                "n_features": int(len(feats)), "groups": feats["group"].value_counts().to_dict(),
                "sizes_mb": sizes, "timings": {"vectorizer_fit_s": fit_s, "transform_s": transform_s,
                                               "total_s": time.perf_counter() - t0},
                "git": git_info(), "environment": environment(),
                "outputs": describe_files(outputs + [out / "feature_names.csv", out / "vectorizer.joblib"])},
               out / "manifest.json")
    print(f"Dynamický tabuľkový dataset: {rel(out)}, {len(feats)} príznakov ({time.perf_counter() - t0:.0f} s)")


def write_statistics(data, X, feats, stats, drift, vec, out: Path):
    tr = data["train"]
    grp = stats.groupby("group").agg(počet=("column", "size"), konštantné=("n_unique", lambda v: int((v == 1).sum())),
                                     medián_podielu_nenulových=("frac_nonzero", "median")).reset_index()
    # n-gramy s najväčším rozdielom výskytu medzi triedami (tréning, iba popis)
    Xtr, ytr = X["train"], tr["label"].to_numpy()
    nv = len(vec.vocab_)
    pres_b = (Xtr[ytr == 0, :nv] > 0).mean(axis=0)
    pres_m = (Xtr[ytr == 1, :nv] > 0).mean(axis=0)
    top = feats.iloc[:nv].assign(benign=pres_b, malware=pres_m, rozdiel=pres_m - pres_b)
    top = top.reindex(top["rozdiel"].abs().sort_values(ascending=False).index).head(20)

    def tbl(df):
        c = list(df.columns)
        lines = ["| " + " | ".join(map(str, c)) + " |", "|" + "---|" * len(c)]
        for _, r in df.iterrows():
            lines.append("| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |")
        return "\n".join(lines)

    drift_txt = "_nevypočítané (chýba niektorá časť)_"
    if drift is not None:
        dg = drift.groupby("group")[["ks_train_validation", "ks_train_test"]].median().reset_index()
        drift_txt = tbl(dg.rename(columns={"ks_train_validation": "KS train–val (medián)", "ks_train_test": "KS train–test (medián)"}))
    text = f"""# Štatistiky dynamického tabuľkového datasetu

> Generované `src/data/build_dynamic_tabular.py` ({now_iso()}). Slovník a štatistiky príznakov iba z tréningu;
> porovnania s validáciou a testom sú popisné.

## Rozmery
{tbl(pd.DataFrame([{"časť": s, "vzorky": len(d), "príznaky": X[s].shape[1]} for s, d in data.items()]))}

## Skupiny príznakov (tréning)
{tbl(grp)}

Slovník: {len(vec.vocab_)} n-gramov API (min. {vec.min_doc_freq} tréningových vzoriek, max. {vec.max_features}),
{len(vec.event_vocab_)} typov udalostí, súhrnné príznaky: {'áno' if vec.include_summary else 'nie'}.

## N-gramy s najväčším rozdielom výskytu medzi triedami (tréning, podiel vzoriek s n-gramom)
{tbl(top[["name", "benign", "malware", "rozdiel"]])}

## Posun rozdelenia príznakov (KS, popisné)
{drift_txt}
"""
    (out / "STATISTICS.md").write_text(text, encoding="utf-8")
    (out / "README.md").write_text(f"""# processed/dynamic/tabular/ – dynamický dataset pre spoločný rebríček

> Generované `src/data/build_dynamic_tabular.py`. Štatistiky: [STATISTICS.md](STATISTICS.md).

## Použité techniky
1. Vstup: normalizovaná cache reportov (`processed/dynamic/cache`) – všetky vstupné body a vlákna vzorky spolu,
   názvy API malými písmenami; poradie vzoriek = spoločný index.
2. Reprezentácia: n-gramy postupnosti API volaní (rozsah {vec.ngram_range}), slovník z **tréningu**
   (min. {vec.min_doc_freq} vzoriek, top {vec.max_features} podľa dokumentovej frekvencie); počty udalostí podľa typu;
   súhrnné príznaky reportu. Hodnoty = surové počty.
3. Učené transformácie modelov (log1p, štandardizácia) sa robia v experimente, ako pri statických dátach.
4. Neznáme n-gramy vo validácii/teste sa ignorujú (nevidené správanie nemá vlastný príznak).

## Obmedzenia
- Reporty pochádzajú z emulácie Speakeasy (limit 500 API volaní na vstupný bod, časový limit 60 s);
  veľká časť vstupných bodov končí chybou emulátora – pozri `processed/dynamic/audit/AUDIT.md`.
- Argumenty API volaní sa v tejto reprezentácii nepoužívajú (sú v cache pre špecifické modely vrstvy B).
""", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(PROCESSED_DIR / "dynamic" / "cache"))
    ap.add_argument("--out", default=None, help="predvolene processed/dynamic/tabular[_<variant>]")
    ap.add_argument("--config", default="configs/data/dynamic.yaml")
    ap.add_argument("--variant", default=None, help="kontrolný variant z tabular_variants (napr. full)")
    a = ap.parse_args()
    out = Path(a.out) if a.out else PROCESSED_DIR / "dynamic" / ("tabular" + (f"_{a.variant}" if a.variant else ""))
    main(Path(a.cache), out, a.config, variant=a.variant)
