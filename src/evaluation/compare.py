"""Porovnanie modelov jedného prístupu: runs/<prístup>/<model>/<posledný beh> -> runs/comparison/<prístup>/.

Spustenie:
    .venv\\Scripts\\python.exe -m src.evaluation.compare --approach static
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.paths import RUNS_DIR, rel
from src.common.provenance import now_iso
from . import plots as P

ORDER = ["lr", "rf", "lightgbm", "mlp_small", "mlp_large"]


def latest_runs(approach: str, runs_root: Path = RUNS_DIR) -> dict[str, Path]:
    out = {}
    for mdir in sorted((runs_root / approach).iterdir()):
        if not mdir.is_dir():
            continue
        runs = sorted(r for r in mdir.iterdir() if (r / "metrics.json").exists())
        if runs:
            out[mdir.name] = runs[-1]
    return out


def collect(runs: dict[str, Path]) -> pd.DataFrame:
    rows = []
    for name, run in runs.items():
        m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
        t = json.loads((run / "timing.json").read_text(encoding="utf-8"))
        S = m["summary"]
        g = lambda split, k: S[split][k]["mean"]
        sd = lambda split, k: S[split][k]["std"]
        trans_ms = t.get("transform_cpu_latency", {}).get("median_ms", 0.0)
        rows.append({
            "model": name, "run": run.name,
            "auc_val": g("validation", "roc_auc"), "auc_test": g("test", "roc_auc"), "auc_test_std": sd("test", "roc_auc"),
            "tpr1_test": g("test", "tpr_at_fpr_0.01"), "tpr1_test_std": sd("test", "tpr_at_fpr_0.01"),
            "tpr01_test": g("test", "tpr_at_fpr_0.001"),
            "f1_test": g("test", "at_val_fpr.f1"), "fpr_test": g("test", "at_val_fpr.fpr"),
            "recall_test": g("test", "at_val_fpr.recall_tpr"),
            "gap_auc": g("train", "roc_auc") - g("validation", "roc_auc"),
            "cpu_ms": t["cpu_latency"]["median_ms"] + trans_ms, "cpu_model_ms": t["cpu_latency"]["median_ms"],
            "cpu_sps": t["cpu_throughput"]["samples_per_s"],
            "gpu_ms": t.get("gpu_latency", {}).get("median_ms", np.nan),
            "params": t["n_parameters"], "size_mb": t["model_disk_bytes"] / 1e6,
            "fit_s": float(np.mean(t["fit_s_per_seed"])), "hpo_min": t["hpo_s"] / 60,
        })
    df = pd.DataFrame(rows)
    df["_o"] = df["model"].map({k: i for i, k in enumerate(ORDER)}).fillna(99)
    return df.sort_values("_o").drop(columns="_o").reset_index(drop=True)


def plot_quality_vs_latency(df: pd.DataFrame, metric: str, label: str, path: Path, title: str):
    fig, ax = P._fig(7.5, 5)
    ax.scatter(df["cpu_ms"], df[metric], s=70, color=P.SPLIT_COLOR["test"], edgecolor=P.SURFACE, linewidth=2, zorder=3)
    for _, r in df.iterrows():
        ax.annotate(r["model"], (r["cpu_ms"], r[metric]), textcoords="offset points", xytext=(8, 4), color=P.INK, fontsize=10)
    ax.set_xscale("log")
    P._style(ax, title, "CPU latencia na vzorku, batch 1, 1 vlákno [ms] (log.)", label)
    P._save(fig, path)


def plot_metric_bars(df: pd.DataFrame, metric: str, std: str, label: str, path: Path, title: str):
    fig, ax = P._fig(7.5, 4.2)
    y = np.arange(len(df))[::-1]
    ax.barh(y, df[metric], xerr=df[std], height=0.6, color=P.SPLIT_COLOR["test"],
            error_kw={"ecolor": P.INK, "capsize": 3, "linewidth": 1})
    for yi, v in zip(y, df[metric]):
        ax.text(v, yi, f"  {v:.4f}", va="center", color=P.INK, fontsize=9)
    lo = max(0.0, df[metric].min() - (df[metric].max() - df[metric].min()) * 1.5 - 0.005)
    ax.set_xlim(lo, min(1.0, df[metric].max() + (df[metric].max() - lo) * 0.25))
    ax.set_yticks(y, df["model"])
    P._style(ax, title, label, "", grid="x")
    P._save(fig, path)


def main(approach: str, runs_root: Path = RUNS_DIR):
    runs = latest_runs(approach, runs_root)
    df = collect(runs)
    out = runs_root / "comparison" / approach
    (out / "plots").mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "summary.csv", index=False)
    plot_quality_vs_latency(df, "auc_test", "ROC-AUC na teste", out / "plots" / "auc_vs_latency.png",
                            f"{approach}: kvalita vs. latencia")
    plot_quality_vs_latency(df, "tpr1_test", "TPR pri FPR 1 % na teste", out / "plots" / "tpr1_vs_latency.png",
                            f"{approach}: detekcia pri FPR 1 % vs. latencia")
    plot_metric_bars(df, "auc_test", "auc_test_std", "ROC-AUC na teste (priemer ± sm. odch. cez seedy)",
                     out / "plots" / "auc_test.png", f"{approach}: ROC-AUC na teste")
    plot_metric_bars(df, "tpr1_test", "tpr1_test_std", "TPR pri FPR 1 % na teste",
                     out / "plots" / "tpr1_test.png", f"{approach}: detekcia pri FPR 1 %")

    def f(v, d=4):
        return "–" if pd.isna(v) else f"{v:.{d}f}"
    lines = ["| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | "
             "gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |",
             "|" + "---|" * 15]
    for _, r in df.iterrows():
        lines.append(f"| [{r['model']}]({'../../' + approach + '/' + r['model'] + '/' + r['run']}/README.md) | {f(r['auc_val'])} | "
                     f"{f(r['auc_test'])} ± {f(r['auc_test_std'])} | {f(r['tpr1_test'])} | {f(r['tpr01_test'])} | "
                     f"{f(r['f1_test'])} | {f(r['fpr_test'])} | {f(r['gap_auc'])} | {f(r['cpu_ms'], 3)} | "
                     f"{r['cpu_sps']:,.0f} | {f(r['gpu_ms'], 3)} | {int(r['params']):,} | {f(r['size_mb'], 2)} | "
                     f"{f(r['fit_s'], 1)} | {f(r['hpo_min'], 1)} |".replace(",", " "))
    text = f"""# Porovnanie modelov – {approach}

> Generované `src/evaluation/compare.py` ({now_iso()}); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \\* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu.

{chr(10).join(lines)}

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
"""
    (out / "README.md").write_text(text, encoding="utf-8")
    print(f"Porovnanie: {rel(out)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="static")
    ap.add_argument("--runs-root", default=None)
    a = ap.parse_args()
    main(a.approach, Path(a.runs_root) if a.runs_root else RUNS_DIR)
