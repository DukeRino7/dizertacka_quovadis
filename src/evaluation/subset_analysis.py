r"""Vyhodnotenie modelov na podskupinách vzoriek podľa výsledku emulácie (docs/04, rozhodnutie 3).

Podskupiny (z processed/dynamic/audit/report_summary.parquet):
- malé reporty (≤ tiny_max_api_calls API volaní),
- emulácia ukončená `unsupported_api` (v teste ~55 %, v tréningu 0 % – stopa inej verzie emulátora),
- ostatné.
Pre každý model (posledný beh) a každú podskupinu: TPR (malvér) a FPR (benign) pri prahu z validácie, priemer cez seedy.
Ukáže, kde dynamická časť zlyháva a či ju statická časť v hybride podrží.

    .venv\Scripts\python.exe -m src.evaluation.subset_analysis --approaches static dynamic hybrid
"""
import argparse
import json

import numpy as np
import pandas as pd

from src.common.config import load_config
from src.common.paths import PROCESSED_DIR, RUNS_DIR, rel
from src.common.provenance import now_iso
from .compare import latest_runs


def subsets(split: str) -> pd.DataFrame:
    d = pd.read_parquet(PROCESSED_DIR / "dynamic" / "audit" / "report_summary.parquet",
                        columns=["sha256", "split", "n_api_calls", "module_entry_error"])
    tiny = load_config("configs/data/dynamic.yaml")["audit"]["tiny_max_api_calls"]
    d = d[d["split"] == split].copy()
    d["podskupina"] = np.where(d["n_api_calls"] <= tiny, f"malý report (≤{tiny} volaní)",
                               np.where(d["module_entry_error"] == "unsupported_api", "ukončené unsupported_api", "ostatné"))
    return d[["sha256", "podskupina"]]


def evaluate_run(run, sub: pd.DataFrame, split: str) -> pd.DataFrame:
    m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
    rows = []
    for r in m["per_seed"]:
        p = run / "predictions" / f"{split}_seed{r['seed']}.parquet"
        if not p.exists():
            continue
        d = pd.read_parquet(p).merge(sub, on="sha256", how="left")
        d["pred"] = d["score"] >= r["thresholds"]["val_fpr"]
        for g, x in d.groupby("podskupina"):
            mal, ben = x[x["label"] == 1], x[x["label"] == 0]
            rows.append({"podskupina": g, "seed": r["seed"], "n_malware": len(mal), "n_benign": len(ben),
                         "TPR": mal["pred"].mean() if len(mal) else np.nan, "FPR": ben["pred"].mean() if len(ben) else np.nan})
    df = pd.DataFrame(rows)
    return df.groupby("podskupina").agg(n_malware=("n_malware", "first"), n_benign=("n_benign", "first"),
                                        TPR=("TPR", "mean"), FPR=("FPR", "mean")).reset_index()


def main(approaches: list[str], split: str = "test"):
    sub = subsets(split)
    blocks = []
    for a in approaches:
        if not (RUNS_DIR / a).exists():
            continue
        for name, run in latest_runs(a).items():
            res = evaluate_run(run, sub, split)
            if not res.empty:
                blocks.append(res.assign(model=f"{a}/{name}"))
    out = RUNS_DIR / "comparison" / "subsets"
    out.mkdir(parents=True, exist_ok=True)
    if not blocks:
        print("žiadne behy na vyhodnotenie"); return
    df = pd.concat(blocks, ignore_index=True)
    df.to_csv(out / f"subsets_{split}.csv", index=False)
    piv = df.pivot_table(index="model", columns="podskupina", values=["TPR", "FPR"])
    piv.columns = [f"{m} – {g}" for m, g in piv.columns]
    counts = df.drop_duplicates("podskupina")[["podskupina", "n_malware", "n_benign"]]

    def tbl(d):
        cols = list(d.columns)
        lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
        for r in d.itertuples(index=False):
            lines.append("| " + " | ".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in r) + " |")
        return "\n".join(lines)
    (out / "README.md").write_text(f"""# Výsledky podľa výsledku emulácie ({split})

> Generované `src/evaluation/subset_analysis.py` ({now_iso()}), výsledky z `{rel(RUNS_DIR)}`.
> Prah z validácie (FPR ≤ 1 %), priemer cez seedy. TPR = zachytený malvér, FPR = falošné poplachy na neškodných.
> Podskupiny podľa auditu dynamických dát (docs/04): malé reporty, emulácia ukončená `unsupported_api`
> (stopa inej verzie emulátora v teste), ostatné.

## Veľkosti podskupín
{tbl(counts)}

## Výsledky
{tbl(piv.reset_index())}
""", encoding="utf-8")
    print(f"Podskupiny: {rel(out)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approaches", nargs="*", default=["static", "dynamic", "hybrid", "students_static", "students_dynamic"])
    ap.add_argument("--split", default="test")
    a = ap.parse_args()
    main(a.approaches, a.split)
