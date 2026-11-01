"""Audit Speakeasy reportov (iba čítanie): kompletnosť sťahovania, párovanie s indexom, poškodené
a prázdne reporty, chyby emulácie, malé reporty (riziko skratky), štatistiky API volaní.

Rozhodnutia o reprezentácii sa robia IBA podľa tréningu; validácia a test sú v reporte iba popisné.

Spustenie (po stiahnutí celého datasetu):
    .venv\\Scripts\\python.exe -m src.data.audit_dynamic
Vývojová kontrola na časti dát (napr. iba stiahnutý test) do iného priečinka:
    .venv\\Scripts\\python.exe -m src.data.audit_dynamic --splits test --out <priečinok> --allow-missing
"""
import argparse
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

from src.common.config import load_config
from src.common.paths import INDEX_DIR, PROCESSED_DIR, SPEAKEASY_DIR, rel, resolve
from src.common.provenance import describe_files, environment, git_info, now_iso, write_json
from src.evaluation import plots as P
from .speakeasy_listing import read_listing
from .speakeasy_source import find_reports, parse_report, summarize

SPLIT_ORDER = ["train", "validation", "test"]


def _work(args):
    path, sha = args
    r = parse_report(SPEAKEASY_DIR / path, sha)
    s = summarize(r)
    names = [n.lower() for n in r.api_names]
    return s, sorted(set(names)), tuple(names[:5])


def parse_all(df: pd.DataFrame, workers: int) -> tuple[pd.DataFrame, list, list]:
    items = list(zip(df["path"], df["sha256"]))
    with ProcessPoolExecutor(max_workers=workers) as ex:
        out = list(ex.map(_work, items, chunksize=64))
    summ = pd.DataFrame([o[0] for o in out])
    return summ, [o[1] for o in out], [o[2] for o in out]


def _q(s: pd.Series) -> str:
    return f"{s.median():.0f} [{s.quantile(0.05):.0f}–{s.quantile(0.95):.0f}]"


def md(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(out)


def main(splits: list[str], out: Path, allow_missing: bool, cfg_path: str):
    t0 = time.perf_counter()
    cfg = load_config(cfg_path)["audit"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "plots").mkdir(exist_ok=True)
    index = pd.read_parquet(INDEX_DIR / "samples.parquet")
    index = index[index["split"].isin(splits)].reset_index(drop=True)

    # 1. kompletnosť sťahovania a párovanie
    listing = read_listing(resolve(load_config(cfg_path)["speakeasy_listing"]))
    disk = find_reports()
    disk_idx = disk.set_index(["sha256", "original_split"])
    lst = listing.set_index(["sha256", "original_split"])
    on_disk = lst.index.isin(disk_idx.index)
    size_ok = pd.Series(False, index=lst.index)
    common = lst.index[on_disk]
    size_ok.loc[common] = disk_idx.loc[common, "bytes"].to_numpy() == lst.loc[common, "speakeasy_bytes"].to_numpy()
    completeness = {
        "listed": int(len(lst)), "on_disk": int(on_disk.sum()), "missing": int((~on_disk).sum()),
        "size_mismatch": int((on_disk & ~size_ok.to_numpy()).sum()),
        "missing_by_split": listing[~on_disk].groupby("original_split").size().to_dict(),
    }
    m = index.merge(disk[["sha256", "original_split", "path", "bytes"]], on=["sha256", "original_split"], how="left")
    missing_idx = m["path"].isna()
    if missing_idx.any() and not allow_missing:
        raise SystemExit(f"{int(missing_idx.sum())} vzoriek indexu nemá report na disku – dokončiť sťahovanie "
                         f"alebo použiť --allow-missing (iba vývoj).")
    m = m[~missing_idx].reset_index(drop=True)

    # 2. načítanie všetkých reportov
    t = time.perf_counter()
    summ, api_sets, prefixes = parse_all(m, cfg["workers"])
    parse_s = time.perf_counter() - t
    d = m[["sha256", "family", "label", "split", "bytes"]].merge(summ, on="sha256", validate="one_to_one")
    d["tiny"] = d["n_api_calls"] <= cfg["tiny_max_api_calls"]
    d["hit_api_limit"] = d["max_api_per_ep"] >= cfg["api_limit"]
    d.to_parquet(out / "report_summary.parquet", index=False)

    # 3. tabuľky
    status = d.pivot_table(index="status", columns="split", values="sha256", aggfunc="count", fill_value=0)
    fam_rows = []
    for (sp, fam), g in d.groupby(["split", "family"]):
        fam_rows.append({"časť": sp, "rodina": fam, "n": len(g), "API volaní medián [p5–p95]": _q(g["n_api_calls"]),
                         f"malé (≤{cfg['tiny_max_api_calls']} volaní)": round(g["tiny"].mean(), 3),
                         "bez API volaní": round((g["n_api_calls"] == 0).mean(), 3),
                         "chyba v module_entry": round(g["module_entry_error"].notna().mean(), 3),
                         f"limit {cfg['api_limit']} vo vstupnom bode": round(g["hit_api_limit"].mean(), 3),
                         "s vláknami": round((g["n_threads"] > 0).mean(), 3),
                         "s udalosťami": round((g["n_events"] > 0).mean(), 3)})
    fam = pd.DataFrame(fam_rows)
    fam["_s"] = fam["časť"].map({k: i for i, k in enumerate(SPLIT_ORDER)})
    fam = fam.sort_values(["_s", "rodina"]).drop(columns="_s")

    err = d.groupby("split")["module_entry_error"].value_counts().rename("n").reset_index()
    err["module_entry_error"] = err["module_entry_error"].str.slice(0, 60)

    # malé reporty: najčastejšie začiatky postupnosti a ich rozdelenie podľa rodín (iba tréning)
    tr = d["split"] == "train"
    pre = pd.Series([" → ".join(p) if p else "(žiadne volanie)" for p in prefixes])
    tiny_tr = d[tr & d["tiny"]].assign(seq=pre[tr & d["tiny"]].values)
    tiny_tab = (tiny_tr.groupby(["seq", "family"]).size().unstack(fill_value=0)
                if len(tiny_tr) else pd.DataFrame())
    if len(tiny_tab):
        tiny_tab["spolu"] = tiny_tab.sum(axis=1)
        tiny_tab = tiny_tab.sort_values("spolu", ascending=False).head(cfg["top_k"]).reset_index()

    # slovník API na tréningu (dokumentová frekvencia)
    df_cnt = Counter()
    for keep, s in zip(tr, api_sets):
        if keep:
            df_cnt.update(s)
    n_tr = int(tr.sum())
    vocab = pd.DataFrame(df_cnt.most_common(), columns=["api", "doc_freq"])
    vocab["doc_share"] = vocab["doc_freq"] / max(n_tr, 1)
    vocab.to_csv(out / "api_vocabulary_train.csv", index=False)
    vocab_info = {"unique_api_train": int(len(vocab)),
                  **{f"api_in_>=_{k}_train_samples": int((vocab["doc_freq"] >= k).sum()) for k in (5, 20, 100)}}

    # 4. grafy
    plot_tiny_share(d, cfg["tiny_max_api_calls"], out / "plots" / "tiny_reports_by_family.png")
    plot_api_calls(d, out / "plots" / "api_calls_by_family.png")

    # 5. report
    write_json({"created": now_iso(), "splits": splits, "completeness": completeness, "vocab": vocab_info,
                "parse_s": parse_s, "duration_s": time.perf_counter() - t0, "config": cfg, "git": git_info(),
                "environment": environment(),
                "outputs": describe_files([out / "report_summary.parquet", out / "api_vocabulary_train.csv"])},
               out / "audit_manifest.json")
    text = f"""# Audit Speakeasy reportov

> Generované `src/data/audit_dynamic.py` ({now_iso()}); časti: {', '.join(splits)}.
> Rozhodnutia o reprezentácii sa robia iba podľa tréningu; validácia a test sú popisné.
> Reporty pochádzajú z **emulácie Speakeasy**, nie z behu v plnohodnotnom Windows sandboxe.

## 1. Kompletnosť sťahovania (voči zoznamu súborov na Hugging Face)
- v zozname: {completeness['listed']}, na disku: {completeness['on_disk']}, chýba: {completeness['missing']}
  {completeness['missing_by_split']}, iná veľkosť než v zozname: {completeness['size_mismatch']}
- vzoriek indexu bez reportu na disku: {int(missing_idx.sum())} {'(spustené s --allow-missing – iba vývoj)' if missing_idx.any() else ''}

## 2. Stav načítania reportov
{md(status.reset_index())}

## 3. Prehľad podľa časti a rodiny
{md(fam)}

## 4. Chyby emulácie v module_entry (najčastejšie)
{md(err.groupby('split').head(6))}

## 5. Malé reporty (≤ {cfg['tiny_max_api_calls']} API volaní) – najčastejšie začiatky postupnosti, iba tréning
{md(tiny_tab) if len(tiny_tab) else '_žiadne_'}

Ak sa niektorá krátka postupnosť vyskytuje takmer iba v jednej rodine, je to **riziko skratky** – model by sa mohol
naučiť „krátky report = táto rodina“ namiesto správania.

## 6. Slovník API (tréning, názvy malými písmenami)
{vocab_info}; úplný zoznam: `api_vocabulary_train.csv`.

Grafy: `plots/tiny_reports_by_family.png`, `plots/api_calls_by_family.png`.
"""
    (out / "AUDIT.md").write_text(text, encoding="utf-8")
    print(f"Audit hotový: {rel(out)} ({time.perf_counter() - t0:.0f} s)")


def plot_tiny_share(d, thr, path):
    t = d.groupby(["family", "split"])["tiny"].mean().unstack() * 100
    fams = ["benign"] + sorted(f for f in t.index if f != "benign")
    splits = [s for s in SPLIT_ORDER if s in t.columns]
    fig, ax = P._fig(7.5, 5)
    h = 0.8 / len(splits)
    y = np.arange(len(fams))[::-1]
    for k, s in enumerate(splits):
        ax.barh(y + (len(splits) / 2 - k - 0.5) * h, t.loc[fams, s], height=h - 0.03, color=P.SPLIT_COLOR[s], label=P.SPLIT_SK[s])
    ax.set_yticks(y, fams)
    P._style(ax, f"Podiel malých reportov (≤ {thr} API volaní)", "podiel vzoriek rodiny [%]", "", grid="x")
    ax.legend(frameon=False, labelcolor=P.INK2, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=len(splits))
    P._save(fig, path)


def plot_api_calls(d, path):
    g = d[d["split"] == "train"] if (d["split"] == "train").any() else d
    fams = ["benign"] + sorted(f for f in g["family"].unique() if f != "benign")
    fig, ax = P._fig(7.5, 5)
    data = [np.log10(g.loc[g["family"] == f, "n_api_calls"].to_numpy() + 1) for f in fams][::-1]
    bp = ax.boxplot(data, orientation="horizontal", patch_artist=True, widths=0.55, showfliers=False,
                    medianprops={"color": P.INK, "linewidth": 1.5}, whiskerprops={"color": P.INK2}, capprops={"color": P.INK2})
    for b in bp["boxes"]:
        b.set(facecolor=P.SPLIT_COLOR["train"], edgecolor=P.SURFACE, linewidth=2)
    ax.set_yticks(np.arange(1, len(fams) + 1), fams[::-1])
    ticks = [0, 1, 2, 3, 4]
    ax.set_xticks(ticks, [f"{10 ** t - 1:,.0f}".replace(",", " ") for t in ticks])
    P._style(ax, f"Počet API volaní na vzorku ({'tréning' if (d['split'] == 'train').any() else 'dostupné dáta'})",
             "počet API volaní (log. mierka)", "", grid="x")
    P._save(fig, path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", nargs="*", default=SPLIT_ORDER)
    ap.add_argument("--out", default=str(PROCESSED_DIR / "dynamic" / "audit"))
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--config", default="configs/data/dynamic.yaml")
    a = ap.parse_args()
    main(a.splits, Path(a.out), a.allow_missing, a.config)
