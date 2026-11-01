"""Predspracovanie statických EMBER príznakov do processed/static.

Predpoklad: existuje processed/index (src/data/build_index.py).
Spustenie (z koreňa projektu):
    .venv\\Scripts\\python.exe -m src.data.build_static --config configs/data/static.yaml

Výstup v processed/static/:
    X_{train,validation,test}.npy     float32 [n, 2381], pôvodné EMBER hodnoty (bez učených transformácií)
    y_{train,validation,test}.npy     int8, 0 = benign, 1 = malware
    meta_{train,validation,test}.parquet  sha256, family, label, feature_group (zarovnané s riadkami X)
    feature_names.csv                 index stĺpca, názov, skupina
    train_feature_stats.parquet       štatistiky príznakov vypočítané IBA na tréningu
    drift_ks.parquet                  popisný posun rozdelenia príznakov (KS) train vs validation/test
    plots/*.png                       grafy
    STATISTICS.md, README.md, manifest.json
"""
import argparse
import time

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.common.config import load_config
from src.common.paths import INDEX_DIR, STATIC_DIR, rel, resolve
from src.common.provenance import describe_files, environment, git_info, now_iso, sha256_file, write_json
from .build_index import SPLIT_ORDER, counts_table, md_table
from .ember_layout import EMBER_DIM, GROUPS, feature_table
from .ember_source import load_rows

# Paleta (dataviz referenčná paleta, svetlý režim): prvé tri kategoriálne sloty + neutrálne tóny.
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = {"train": "#2a78d6", "validation": "#eb6834", "test": "#1baf7a"}
SPLIT_SK = {"train": "train", "validation": "validácia", "test": "test"}


# ----------------------------------------------------------------------------- štatistiky

def column_stats(X: np.ndarray, chunk: int = 128) -> pd.DataFrame:
    """Štatistiky po stĺpcoch (počítané po blokoch, aby sa šetrila pamäť)."""
    n, d = X.shape
    q_levels = [0.01, 0.5, 0.99]
    rows = []
    for start in range(0, d, chunk):
        C = np.sort(np.asarray(X[:, start:start + chunk], dtype=np.float64), axis=0)
        mean, std = C.mean(axis=0), C.std(axis=0)
        qs = np.quantile(C, q_levels, axis=0, method="linear")
        nonzero = (C != 0).mean(axis=0)
        for j in range(C.shape[1]):
            col = C[:, j]
            change = np.flatnonzero(np.diff(col) != 0)
            runs = np.diff(np.concatenate([[-1], change, [n - 1]]))
            rows.append((start + j, col[0], col[-1], mean[j], std[j], qs[0, j], qs[1, j], qs[2, j],
                         nonzero[j], len(runs), runs.max() / n))
    return pd.DataFrame(rows, columns=["column", "min", "max", "mean", "std", "q01", "median", "q99",
                                       "frac_nonzero", "n_unique", "top_value_frac"])


def ks_statistic(a: np.ndarray, b: np.ndarray) -> float:
    """Dvojvýberová Kolmogorov-Smirnovova štatistika D (max. rozdiel empirických distribučných funkcií)."""
    a, b = np.sort(a), np.sort(b)
    grid = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, grid, side="right") / len(a)
    cdf_b = np.searchsorted(b, grid, side="right") / len(b)
    return float(np.max(np.abs(cdf_a - cdf_b)))


def drift_table(X: dict, cfg: dict, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    k = cfg["max_rows_per_split"]
    sub = {s: np.asarray(X[s][np.sort(rng.choice(len(X[s]), min(k, len(X[s])), replace=False))])
           for s in SPLIT_ORDER}
    rows = [(j, ks_statistic(sub["train"][:, j], sub["validation"][:, j]),
             ks_statistic(sub["train"][:, j], sub["test"][:, j])) for j in range(EMBER_DIM)]
    return pd.DataFrame(rows, columns=["column", "ks_train_validation", "ks_train_test"])


# ----------------------------------------------------------------------------- grafy

def _style(ax, title: str, xlabel: str = "", ylabel: str = ""):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", color=INK, fontsize=12, pad=10)
    ax.set_xlabel(xlabel, color=INK2)
    ax.set_ylabel(ylabel, color=INK2)
    ax.tick_params(colors=INK2, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def plot_class_distribution(index: pd.DataFrame, path):
    t = counts_table(index).drop(index="SPOLU")
    share = t / t.sum() * 100
    fams = list(share.index)[::-1]
    fig, ax = plt.subplots(figsize=(8, 5.5), facecolor=SURFACE)
    h = 0.26
    y = np.arange(len(fams))
    for i, s in enumerate(SPLIT_ORDER):
        ax.barh(y + (1 - i) * h, share.loc[fams, s], height=h - 0.03, color=SERIES[s],
                label=f"{SPLIT_SK[s]} (n = {int(t[s].sum()):,})".replace(",", " "))
    ax.set_yticks(y, fams)
    _style(ax, "Zloženie častí rozdelenia podľa rodiny", "podiel vzoriek v časti [%]")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_drift_by_group(drift: pd.DataFrame, feats: pd.DataFrame, path):
    d = drift.merge(feats, on="column")
    groups = [g.name for g in GROUPS][::-1]
    fig, ax = plt.subplots(figsize=(8, 5.5), facecolor=SURFACE)
    pos = np.arange(len(groups))
    for off, col, s in [(0.18, "ks_train_validation", "validation"), (-0.18, "ks_train_test", "test")]:
        data = [d.loc[d["group"] == g, col].to_numpy() for g in groups]
        bp = ax.boxplot(data, positions=pos + off, widths=0.3, orientation="horizontal", patch_artist=True,
                        showfliers=False, medianprops={"color": INK, "linewidth": 1.5},
                        whiskerprops={"color": INK2}, capprops={"color": INK2})
        for b in bp["boxes"]:
            b.set(facecolor=SERIES[s], edgecolor=SURFACE, linewidth=2)
        ax.plot([], [], color=SERIES[s], linewidth=8, label=f"train vs {SPLIT_SK[s]}")
    ax.set_yticks(pos, groups)
    _style(ax, "Posun rozdelenia príznakov podľa skupiny (KS štatistika)", "KS štatistika D (0 = zhoda)")
    ax.legend(frameon=False, labelcolor=INK2, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_sparsity(stats: pd.DataFrame, feats: pd.DataFrame, path):
    d = stats.merge(feats, on="column")
    groups = [g.name for g in GROUPS][::-1]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    data = [d.loc[d["group"] == g, "frac_nonzero"].to_numpy() * 100 for g in groups]
    bp = ax.boxplot(data, orientation="horizontal", patch_artist=True, showfliers=True, widths=0.55,
                    medianprops={"color": INK, "linewidth": 1.5}, whiskerprops={"color": INK2},
                    capprops={"color": INK2}, flierprops={"marker": "o", "markersize": 3,
                                                          "markerfacecolor": INK2, "markeredgecolor": "none"})
    for b in bp["boxes"]:
        b.set(facecolor=SERIES["train"], edgecolor=SURFACE, linewidth=2)
    ax.set_yticks(np.arange(1, len(groups) + 1), groups)
    _style(ax, "Podiel nenulových hodnôt príznakov na tréningu (podľa skupiny)",
           "podiel nenulových hodnôt v stĺpci [%]")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------------- reporty

def _fmt(v, digits=4):
    if isinstance(v, (int, np.integer)):
        return f"{v:,}".replace(",", " ")
    if isinstance(v, (float, np.floating)):
        return f"{v:.{digits}g}"
    return str(v)


def _tbl(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(_fmt(v) for v in r) + " |")
    return "\n".join(out)


def write_statistics(index, stats, drift, feats, checks, cfg, manifest, path):
    s = stats.merge(feats, on="column")
    near = cfg["near_constant_threshold"]
    g_rows = []
    for g in GROUPS:
        part = s[s["group"] == g.name]
        tail = (part["max"] / part["q99"].where(part["q99"] > 0)).median()
        g_rows.append({"skupina": g.name, "šírka": g.width, "typ": g.kind,
                       "konštantné (train)": int((part["n_unique"] == 1).sum()),
                       f"takmer konšt. (≥{near})": int((part["top_value_frac"] >= near).sum()),
                       "medián podielu nenul.": float(part["frac_nonzero"].median()),
                       "min": float(part["min"].min()), "max": float(part["max"].max()),
                       "medián max/q99": float(tail) if pd.notna(tail) else "–"})
    g_tbl = pd.DataFrame(g_rows)
    neg_groups = ", ".join(f"`{g}`" for g in g_tbl.loc[g_tbl["min"] < 0, "skupina"])

    d = drift.merge(feats, on="column")
    d_grp = d.groupby("group", sort=False)[["ks_train_validation", "ks_train_test"]].agg(["median", "max"])
    d_grp.columns = ["val: medián", "val: max", "test: medián", "test: max"]
    d_grp = d_grp.reindex([g.name for g in GROUPS]).reset_index().rename(columns={"group": "skupina"})
    top = d.sort_values("ks_train_test", ascending=False).head(cfg["drift"]["top_k"])[
        ["column", "name", "group", "ks_train_test", "ks_train_validation"]]

    interp = ["general_size", "general_vsize", "general_has_signature", "general_imports",
              "strings_entropy", "section_num", "header_coff_timestamp"]
    sel = feats.set_index("name").loc[interp, "column"]
    med_rows = []
    for split in SPLIT_ORDER:
        X = np.load(STATIC_DIR / f"X_{split}.npy", mmap_mode="r")
        y = np.load(STATIC_DIR / f"y_{split}.npy")
        for lab, lname in [(0, "benign"), (1, "malware")]:
            vals = np.asarray(X[y == lab][:, sel.to_numpy()], dtype=np.float64)
            med_rows.append({"časť": SPLIT_SK[split], "trieda": lname,
                             **{n: float(np.median(vals[:, i])) for i, n in enumerate(interp)}})
    med = pd.DataFrame(med_rows)

    sizes = manifest["sizes_mb"]
    text = f"""# Štatistiky statického datasetu (EMBER)

> Automaticky generované skriptom `src/data/build_static.py` ({manifest['created']}).
> Všetky čísla pochádzajú priamo z dát v `processed/static`. Štatistiky príznakov (časť 3) sú počítané
> **iba na tréningu**. Porovnania s validáciou a testom (časti 4–5) sú iba popisné a nevyužívajú sa
> na žiadne rozhodnutie o spracovaní ani modeloch.

## 1. Rozmery a integrita
| časť | vzorky | príznaky | NaN | ±Inf | veľkosť X [MB] |
|---|---|---|---|---|---|
""" + "\n".join(
        f"| {SPLIT_SK[sp]} | {_fmt(checks[sp]['rows'])} | {EMBER_DIM} | {checks[sp]['nan']} | {checks[sp]['inf']} | {sizes[sp]:.0f} |"
        for sp in SPLIT_ORDER) + f"""

- Typ: float32; riadky zoradené podľa `processed/index/samples.parquet` (časť → rodina → SHA-256).
- Overené: poradie SHA-256 v `meta_*.parquet` sa zhoduje s indexom; každý riadok X je zhodný s pôvodným
  `features.npy` (kontrola na {checks['verified_rows']} náhodných riadkoch, max. odchýlka {checks['max_abs_diff']}).

## 2. Vzorky podľa rodiny a časti
{md_table(counts_table(index), 'rodina')}

Podiel malvéru: """ + ", ".join(
        f"{SPLIT_SK[sp]} {index.loc[index['split'] == sp, 'label'].mean():.3f}" for sp in SPLIT_ORDER) + f"""

Graf: `plots/class_distribution.png`

## 3. Príznaky podľa skupín (iba tréning)
{_tbl(g_tbl)}

- *konštantné* = jediná hodnota na celom tréningu (pre model bez informácie); spolu
  **{int((stats['n_unique'] == 1).sum())}** z {EMBER_DIM}.
- *takmer konšt.* = najčastejšia hodnota pokrýva aspoň {near} tréningových vzoriek; spolu
  **{int((stats['top_value_frac'] >= near).sum())}**.
- *medián max/q99* = typický pomer maxima a 99. percentilu v stĺpci; vysoké hodnoty znamenajú ťažké chvosty
  (dôvod pre log-transformáciu pri lineárnych modeloch a neurónových sieťach).
- Záporné hodnoty sa vyskytujú v skupinách: {neg_groups} (hašované bloky používajú znamienkový FeatureHasher).

Graf: `plots/feature_sparsity_by_group.png`; úplná tabuľka: `train_feature_stats.parquet`.

## 4. Posun rozdelenia príznakov (popisné)
Dvojvýberová KS štatistika D po príznakoch, náhodná podvzorka max. {cfg['drift']['max_rows_per_split']} vzoriek z každej časti
(seed {manifest['seed']}). Validácia je náhodne vyčlenená z rovnakého obdobia ako tréning, preto slúži ako referencia
„bez posunu“; test je zozbieraný o 3 mesiace neskôr.

{_tbl(d_grp)}

Najväčší posun train → test ({cfg['drift']['top_k']} príznakov):

{_tbl(top.rename(columns={'column': 'stĺpec', 'name': 'príznak', 'group': 'skupina', 'ks_train_test': 'KS train–test', 'ks_train_validation': 'KS train–val'}))}

Graf: `plots/drift_ks_by_group.png`; úplná tabuľka: `drift_ks.parquet`.

## 5. Mediány vybraných interpretovateľných príznakov
{_tbl(med)}

- `header_coff_timestamp` je čas zostavenia z hlavičky PE (dá sa ľahko sfalšovať); pri interpretácii modelov
  sledovať, či sa naň model neopiera ako na časový artefakt zberu dát.

## 6. Duplicity
- SHA-256 je v rámci datasetu unikátne (prekryv train/test vyriešený v indexe, pozri `processed/index/README.md`).
- Identické EMBER vektory pri rôznych SHA-256: {int((index['feature_group'].value_counts() > 1).sum())} skupín,
  {int(index['feature_group'].map(index['feature_group'].value_counts()).gt(1).sum())} vzoriek; žiadna skupina neprechádza cez viac častí a žiadna nemá rozporné označenie.
"""
    path.write_text(text, encoding="utf-8")


def write_readme(manifest, path):
    text = f"""# processed/static/ – predspracovaný statický dataset (EMBER)

> Generované skriptom `src/data/build_static.py` ({manifest['created']}), konfigurácia `{manifest['config_path']}`.
> Neupravovať ručne. Znovuvytvorenie: `.venv\\Scripts\\python.exe -m src.data.build_static`.
> Štatistiky datasetu: [STATISTICS.md](STATISTICS.md).

## Súbory
| Súbor | Obsah |
|---|---|
| `X_<časť>.npy` | float32 [n, 2381], pôvodné EMBER hodnoty, časti `train`, `validation`, `test` |
| `y_<časť>.npy` | int8, 0 = benign, 1 = malware |
| `meta_<časť>.parquet` | `sha256`, `family`, `label`, `feature_group` – riadok i patrí k riadku i v X |
| `feature_names.csv` | `column`, `group`, `name` pre všetkých 2381 príznakov |
| `train_feature_stats.parquet` | štatistiky každého príznaku na tréningu (min, max, priemer, smer. odchýlka, kvantily, podiel nenulových, počet unikátnych hodnôt) |
| `drift_ks.parquet` | KS štatistika train–validácia a train–test pre každý príznak (iba popisné) |
| `plots/` | grafy k STATISTICS.md |
| `manifest.json` | konfigurácia, commit, prostredie, kontrolné súčty, časy spracovania |

Načítanie v kóde: `from src.data.static_dataset import load_split` → `load_split("train")` vráti `X`, `y`, `meta`
(X ako memory-map, nenačíta sa celé do RAM).

## Použité techniky spracovania
1. **Spoločný index a rozdelenie** (`processed/index`): jedna vzorka = jeden SHA-256; validácia vyčlenená
   z pôvodného tréningu stratifikovane podľa rodiny a so skupinami identických vektorov držanými spolu
   (`StratifiedGroupKFold`, seed {manifest['seed']}); pôvodný časový test bez zmeny; odstránený prekryv
   train/test podľa SHA-256 (detaily a NÁVRHY v `processed/index/README.md`).
2. **Správne mapovanie riadkov**: riadok v pôvodnom `features.npy` sa určuje indexom z `hashes.txt`;
   nulové riadky zlyhaných extrakcií sa vynechávajú. Integrita overená pri čítaní (pozri `src/data/ember_source.py`).
3. **Kontrola hodnôt**: NaN a ±Inf (žiadne neboli nájdené – pozri STATISTICS.md), zhoda s pôvodnými dátami na náhodnej vzorke.
4. **Materializácia po častiach**: samostatné súbory pre train/validáciu/test → modely nikdy omylom
   nevidia test pri tréningu; formát `.npy` umožňuje rýchle načítanie cez memory-map.
5. **Popis príznakov**: názvy a skupiny podľa rozloženia EMBER v2 (`src/data/ember_layout.py`).
6. **Štatistiky iba z tréningu**: konštantné a takmer konštantné príznaky, rozsahy, ťažké chvosty, riedkosť.
7. **Popisná analýza posunu** train → test (KS), referenčne train → validácia.
8. **Pôvod a reprodukovateľnosť**: `manifest.json` (konfigurácia, git commit, verzie knižníc,
   SHA-256 vstupov aj výstupov, čas spracovania).

## Čo sa zámerne NErobí na uloženom datasete
- **Žiadna škálovanie, log-transformácia ani výber príznakov.** Sú to učené transformácie; robia sa až
  v experimente, fitované iba na tréningu (`src/data/static_transforms.py: StaticPreprocessor`)
  a ukladajú sa s modelom v `runs/`. Stromové modely ich nepotrebujú. Uložené dáta tak zostávajú
  neutrálne pre všetky modely.
- **Žiadne odstránenie konštantných príznakov** – informácia je v `train_feature_stats.parquet`;
  rozhodnutie patrí modelu/experimentu, aby všetky modely mali rovnaký vstup 2381 príznakov.
- **Žiadne vyvažovanie tried** (oversampling/undersampling) – prípadné váhy tried sa nastavujú v experimente.
- **Žiadne úpravy testu** – test sa nepoužíva na ladenie.

## Obmedzenia
- EMBER príznaky boli extrahované autormi datasetu; pôvodné PE súbory nie sú k dispozícii, preto
  **čas extrakcie statických príznakov sa nedá v tomto projekte zmerať** priamo z dát.
- 366 súborov z pôvodného datasetu nemá EMBER príznaky (zlyhaná extrakcia) – nie sú v indexe.
"""
    path.write_text(text, encoding="utf-8")


# ----------------------------------------------------------------------------- hlavný postup

def main(config_path: str) -> None:
    t_all = time.perf_counter()
    timings = {}
    cfg = load_config(config_path)
    index_cfg = load_config("configs/data/index.yaml")
    seed = index_cfg["seed"]
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    (STATIC_DIR / "plots").mkdir(exist_ok=True)
    dtype = np.dtype(cfg["dtype"])

    index = pd.read_parquet(INDEX_DIR / "samples.parquet")
    feats = feature_table()
    feats.to_csv(STATIC_DIR / "feature_names.csv", index=False)

    X, checks, outputs, sizes = {}, {}, [], {}
    rng = np.random.default_rng(seed)
    t = time.perf_counter()
    for split in SPLIT_ORDER:
        part = index[index["split"] == split].reset_index(drop=True)
        Xs = load_rows(part, dtype=dtype)
        checks[split] = {"rows": len(part), "nan": int(np.isnan(Xs).sum()), "inf": int(np.isinf(Xs).sum())}
        if checks[split]["nan"] or checks[split]["inf"]:
            raise ValueError(f"{split}: NaN/Inf v príznakoch – treba rozhodnúť o ošetrení")
        for name, obj in [(f"X_{split}.npy", Xs), (f"y_{split}.npy", part["label"].to_numpy(np.int8))]:
            np.save(STATIC_DIR / name, obj)
            outputs.append(STATIC_DIR / name)
        part[["sha256", "family", "label", "feature_group"]].to_parquet(STATIC_DIR / f"meta_{split}.parquet", index=False)
        outputs.append(STATIC_DIR / f"meta_{split}.parquet")
        sizes[split] = (STATIC_DIR / f"X_{split}.npy").stat().st_size / 1e6
        del Xs
    timings["materialize_s"] = round(time.perf_counter() - t, 1)

    # nezávislá kontrola: náhodné riadky porovnať priamo s pôvodnými súbormi
    t = time.perf_counter()
    max_diff, verified = 0.0, 0
    for split in SPLIT_ORDER:
        Xs = np.load(STATIC_DIR / f"X_{split}.npy", mmap_mode="r")
        meta = pd.read_parquet(STATIC_DIR / f"meta_{split}.parquet")
        part = index[index["split"] == split].reset_index(drop=True)
        assert (meta["sha256"].to_numpy() == part["sha256"].to_numpy()).all()
        for i in rng.choice(len(part), 200, replace=False):
            src = np.load(resolve(part.at[i, "ember_file"]), mmap_mode="r")[part.at[i, "ember_row"]]
            max_diff = max(max_diff, float(np.abs(np.asarray(Xs[i]) - src).max()))
            verified += 1
        X[split] = Xs
    if max_diff != 0.0:
        raise ValueError(f"Uložené dáta sa líšia od pôvodných (max. rozdiel {max_diff})")
    checks.update(verified_rows=verified, max_abs_diff=max_diff)
    timings["verify_s"] = round(time.perf_counter() - t, 1)

    t = time.perf_counter()
    stats = column_stats(X["train"])
    stats.to_parquet(STATIC_DIR / "train_feature_stats.parquet", index=False)
    timings["train_stats_s"] = round(time.perf_counter() - t, 1)

    t = time.perf_counter()
    drift = drift_table(X, cfg["drift"], seed)
    drift.to_parquet(STATIC_DIR / "drift_ks.parquet", index=False)
    timings["drift_s"] = round(time.perf_counter() - t, 1)

    plot_class_distribution(index, STATIC_DIR / "plots" / "class_distribution.png")
    plot_drift_by_group(drift, feats, STATIC_DIR / "plots" / "drift_ks_by_group.png")
    plot_sparsity(stats, feats, STATIC_DIR / "plots" / "feature_sparsity_by_group.png")

    manifest = {
        "created": now_iso(),
        "script": "src/data/build_static.py",
        "config_path": rel(resolve(config_path)),
        "config": cfg,
        "seed": seed,
        "git": git_info(),
        "environment": environment(),
        "inputs": {"index_samples_sha256": sha256_file(INDEX_DIR / "samples.parquet"),
                   "index_manifest": "processed/index/manifest.json"},
        "checks": checks,
        "sizes_mb": sizes,
    }
    write_statistics(index, stats, drift, feats, checks, cfg, manifest, STATIC_DIR / "STATISTICS.md")
    write_readme(manifest, STATIC_DIR / "README.md")
    outputs += [STATIC_DIR / f for f in ["feature_names.csv", "train_feature_stats.parquet", "drift_ks.parquet"]]
    outputs += sorted((STATIC_DIR / "plots").glob("*.png"))
    t = time.perf_counter()
    manifest["outputs"] = describe_files(outputs)
    timings["checksums_s"] = round(time.perf_counter() - t, 1)
    timings["total_s"] = round(time.perf_counter() - t_all, 1)
    manifest["timings"] = timings
    write_json(manifest, STATIC_DIR / "manifest.json")
    print("Statický dataset hotový:", {s: checks[s]["rows"] for s in SPLIT_ORDER}, timings)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/data/static.yaml")
    main(ap.parse_args().config)
