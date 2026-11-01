r"""Záverečné porovnanie prístupov k výskumným otázkam (docs/00_vyskumne_otazky.md) -> runs/comparison/final/.

Spája: vybrané najlepšie modely (runs/selection), študentov, kaskády (runs/cascade) a merania spotreby (benchmark.json).
Všetko na TESTE pri prahoch určených na validácii (FPR <= 1 %). Iba čísla – interpretácia patrí do textu práce.

    .venv\Scripts\python.exe -m src.evaluation.final_report
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.cascade.components import Component
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import now_iso
from . import plots as P

SINGLE = [  # (popis, komponent)
    ("najlepší statický", "auto:static"), ("najlepší dynamický", "auto:dynamic"), ("najlepší hybrid", "auto:hybrid"),
    ("hybrid two_branch", "hybrid/two_branch"),
    ("študent statický (destilácia)", "students_static/mlp_kd"), ("študent statický (bez destilácie)", "students_static/mlp_nokd"),
    ("študent statický (variant A)", "students_static/mlp_kd_modal"),
    ("študent dynamický (destilácia)", "students_dynamic/mlp_kd"), ("študent dynamický (bez destilácie)", "students_dynamic/mlp_nokd"),
    ("študent dynamický (variant A)", "students_dynamic/mlp_kd_modal"),
]
CASCADES = ["main", "nokd", "modal", "heavy", "baselines"]


def _single_row(label, spec):
    try:
        c = Component(spec)
    except FileNotFoundError:
        return None
    S = c.metrics["summary"]["test"]
    cost = c.cost() or {}
    return {"prístup": label, "model": c.metrics["approach"] + "/" + c.metrics["name"],
            "TPR (prah z val.)": S["at_val_fpr.recall_tpr"]["mean"], "FPR (prah z val.)": S["at_val_fpr.fpr"]["mean"],
            "F1": S["at_val_fpr.f1"]["mean"], "TPR@FPR 1 %": S["tpr_at_fpr_0.01"]["mean"],
            "TPR@FPR 0,1 %": S["tpr_at_fpr_0.001"]["mean"], "ROC-AUC": S["roc_auc"]["mean"],
            "CPU ms/vz.": cost.get("cpu_ms_batch"), "latencia ms": cost.get("latency_ms"), "eskalácie": None}


def _cascade_rows(variant):
    base = RUNS_DIR / "cascade" / variant
    runs = sorted(r for r in base.iterdir() if (r / "metrics.json").exists()) if base.exists() else []
    if not runs:
        return []
    m = json.loads((runs[-1] / "metrics.json").read_text(encoding="utf-8"))
    S = m["summary"]["test"]
    costs = {r["meranie"]: r for r in (m.get("costs") or [])}
    cb, lat = costs.get("CPU čas ms/vz. (dávka)", {}), costs.get("latencia ms (1 vz., postupne)", {})
    rows = [{"prístup": f"kaskáda {variant}", "model": f"cascade/{variant}",
             "TPR (prah z val.)": S["cascade"]["recall_tpr"][0], "FPR (prah z val.)": S["cascade"]["fpr"][0],
             "F1": S["cascade"]["f1"][0], "CPU ms/vz.": cb.get("kaskáda (odhad)"), "latencia ms": lat.get("kaskáda (odhad)"),
             "eskalácie": S["_escalation_rate"]}]
    if variant == "main":
        for k, lab in [("late_fusion_mean", "neskorá fúzia (priemer)"), ("late_fusion_stacking", "neskorá fúzia (stacking)")]:
            rows.append({"prístup": lab, "model": "fúzia študentov main", "TPR (prah z val.)": S[k]["recall_tpr"][0],
                         "FPR (prah z val.)": S[k]["fpr"][0], "F1": S[k]["f1"][0],
                         "CPU ms/vz.": cb.get("neskorá fúzia"), "latencia ms": lat.get("neskorá fúzia"), "eskalácie": None})
    return rows


def _fmt(v, d=4):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else (f"{v:.{d}f}" if isinstance(v, float) else str(v))


def _table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        lines.append("| " + " | ".join(_fmt(v) for v in r) + " |")
    return "\n".join(lines)


def _delta(df, a, b, cols):
    A, B = df[df["prístup"] == a], df[df["prístup"] == b]
    if A.empty or B.empty:
        return f"- {a} vs. {b}: _chýbajú výsledky_"
    parts = []
    for c in cols:
        x, y = A.iloc[0][c], B.iloc[0][c]
        if x is not None and y is not None and not (isinstance(x, float) and np.isnan(x)) and not (isinstance(y, float) and np.isnan(y)):
            parts.append(f"{c}: {x:.4f} vs. {y:.4f} (Δ {x - y:+.4f})" if c != "CPU ms/vz." else
                         f"CPU: {x:.4f} vs. {y:.4f} ms ({x / y:.2f}×)" if y else "")
    return f"- **{a}** vs. **{b}**: " + "; ".join(p for p in parts if p)


def plot_quality_cost(df, path):
    d = df.dropna(subset=["CPU ms/vz.", "F1"])
    if d.empty:
        return False
    fig, ax = P._fig(8.5, 5.5)
    casc = d["prístup"].str.startswith("kaskáda")
    ax.scatter(d.loc[~casc, "CPU ms/vz."], d.loc[~casc, "F1"], s=60, color=P.SPLIT_COLOR["train"], edgecolor=P.SURFACE,
               linewidth=1.5, label="jednotlivé modely / fúzia", zorder=3)
    ax.scatter(d.loc[casc, "CPU ms/vz."], d.loc[casc, "F1"], s=90, marker="D", color=P.SPLIT_COLOR["validation"],
               edgecolor=P.SURFACE, linewidth=1.5, label="kaskády", zorder=4)
    for _, r in d.iterrows():
        ax.annotate(r["prístup"], (r["CPU ms/vz."], r["F1"]), textcoords="offset points", xytext=(6, 4), fontsize=8, color=P.INK)
    ax.set_xscale("log")
    P._style(ax, "Kvalita vs. výpočtové nároky (test, prah z validácie)", "CPU čas na vzorku [ms] (log.)", "F1")
    ax.legend(frameon=False, labelcolor=P.INK2, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2)
    P._save(fig, path)
    return True


def main():
    rows = [r for r in (_single_row(l, s) for l, s in SINGLE) if r]
    for v in CASCADES:
        rows += _cascade_rows(v)
    df = pd.DataFrame(rows)
    out = RUNS_DIR / "comparison" / "final"
    (out / "plots").mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "summary.csv", index=False)
    has_plot = plot_quality_cost(df, out / "plots" / "quality_vs_cost.png")
    sel = {g: json.loads((RUNS_DIR / "selection" / f"{g}.json").read_text(encoding="utf-8"))["chosen"]
           for g in ("static", "dynamic", "hybrid") if (RUNS_DIR / "selection" / f"{g}.json").exists()}
    q = ["F1", "TPR (prah z val.)", "FPR (prah z val.)", "CPU ms/vz."]
    text = f"""# Záverečné porovnanie – výskumné otázky

> Generované `src/evaluation/final_report.py` ({now_iso()}), výsledky z `{rel(RUNS_DIR)}`.
> Test (apríl 2022), prahy z validácie (FPR ≤ 1 %), priemer cez seedy. Nároky = benchmark (CPU čas na vzorku, dávka);
> pri kaskáde odhad statický + dynamický + podiel eskalácií × hybrid. Merania nárokov porovnávať iba z jedného počítača.

Vybrané modely (pravidlo `configs/selection.yaml`): {', '.join(f'{g} = `{c}`' for g, c in sel.items()) or '_výber ešte neprebehol_'}

## Všetky prístupy
{_table(df.drop(columns=['model']))}

{'![kvalita vs nároky](plots/quality_vs_cost.png)' if has_plot else ''}

## Otázka 1 – najlepší hybrid
Pozri `{rel(RUNS_DIR / 'selection' / 'hybrid.md')}` a `runs/comparison/hybrid/README.md`.

## Otázka 2 – študenti
{_delta(df, 'študent statický (destilácia)', 'študent statický (bez destilácie)', q)}
{_delta(df, 'študent dynamický (destilácia)', 'študent dynamický (bez destilácie)', q)}
{_delta(df, 'študent statický (destilácia)', 'najlepší statický', q)}
{_delta(df, 'študent dynamický (destilácia)', 'najlepší dynamický', q)}

## Otázka 3 – samostatné prístupy vs. hybrid
{_delta(df, 'najlepší statický', 'najlepší hybrid', q)}
{_delta(df, 'najlepší dynamický', 'najlepší hybrid', q)}

## Otázka 4 – kaskáda
(a) vs. hybrid na každej vzorke:
{_delta(df, 'kaskáda main', 'najlepší hybrid', q)}

(b) vs. samostatné modely:
{_delta(df, 'kaskáda main', 'najlepší statický', q)}
{_delta(df, 'kaskáda main', 'najlepší dynamický', q)}

Doplnkovo: {_delta(df, 'kaskáda main', 'kaskáda nokd', q)[2:]}
{_delta(df, 'kaskáda main', 'neskorá fúzia (stacking)', q)}
{_delta(df, 'kaskáda heavy', 'hybrid two_branch', q)}
"""
    (out / "README.md").write_text(text, encoding="utf-8")
    print(f"Záverečné porovnanie: {rel(out)}")


if __name__ == "__main__":
    main()
