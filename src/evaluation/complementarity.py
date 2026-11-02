"""Analýza komplementarity: ktoré chyby statického modelu opraví hybridný alebo dynamický model (test).

Iba čítanie uložených predikcií vybraných modelov (`selection/*.json`); prahy sa určujú na validácii
(FPR <= 1 %), test sa na nič nenastavuje.
Spustenie: .venv\\Scripts\\python.exe -m src.evaluation.complementarity --runs-root runs_final
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.evaluation.metrics import threshold_for_fpr


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(out)


def load(run: Path, split: str, seed: int) -> pd.DataFrame:
    return pd.read_parquet(run / "predictions" / f"{split}_seed{seed}.parquet").set_index("sha256")


def decisions(run: Path, seed: int, fpr: float) -> pd.Series:
    v, t = load(run, "validation", seed), load(run, "test", seed)
    thr = threshold_for_fpr(v["label"].to_numpy(), v["score"].to_numpy(), fpr)
    return (t["score"] >= thr).astype(int)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", default="runs_final")
    ap.add_argument("--fpr", type=float, default=0.01)
    a = ap.parse_args()
    root = Path(a.runs_root)
    runs = {}
    for k in ("static", "dynamic", "hybrid"):
        sel = json.loads((root / "selection" / f"{k}.json").read_text(encoding="utf-8"))
        runs[k] = Path(sel["chosen_run"])
    rows, fam_rows = [], []
    for seed in (0, 1, 2):
        ref = load(runs["static"], "test", seed)
        y, fam = ref["label"], ref["family"]
        ok = {k: decisions(r, seed, a.fpr).reindex(ref.index) == y for k, r in runs.items()}
        for name, mask in {"malware": y == 1, "benign": y == 0}.items():
            s_err, h_err, d_err = mask & ~ok["static"], mask & ~ok["hybrid"], mask & ~ok["dynamic"]
            rows.append({
                "seed": seed, "trieda": name, "n": int(mask.sum()),
                "chyby statický": int(s_err.sum()),
                "chyby dynamický": int(d_err.sum()),
                "chyby hybrid": int(h_err.sum()),
                "hybrid opraví chybu statického": int((s_err & ok["hybrid"]).sum()),
                "hybrid pokazí správne statického": int((mask & ok["static"] & h_err).sum()),
                "dynamický správne pri chybe statického": int((s_err & ok["dynamic"]).sum()),
                "chyba všetkých troch": int((s_err & h_err & d_err).sum()),
            })
        if seed == 0:
            for f in sorted(fam.unique()):
                m = fam == f
                fam_rows.append({
                    "rodina": f, "n": int(m.sum()),
                    "chyby statický": int((m & ~ok["static"]).sum()),
                    "chyby dynamický": int((m & ~ok["dynamic"]).sum()),
                    "chyby hybrid": int((m & ~ok["hybrid"]).sum()),
                    "dynamický správne pri chybe statického": int((m & ~ok["static"] & ok["dynamic"]).sum()),
                })
    out = root / "comparison" / "complementarity"
    out.mkdir(parents=True, exist_ok=True)
    df, fdf = pd.DataFrame(rows), pd.DataFrame(fam_rows)
    df.to_csv(out / "per_seed.csv", index=False)
    fdf.to_csv(out / "per_family_seed0.csv", index=False)
    agg = df.groupby("trieda").mean(numeric_only=True).drop(columns="seed").round(1)
    lines = [
        "# Komplementarita statického, dynamického a hybridného modelu (test)", "",
        "> Generované `src/evaluation/complementarity.py`. Vybrané modely z `selection/`; prah z validácie "
        f"(FPR ≤ {a.fpr:.0%}), test sa na nič nenastavuje. Počty vzoriek, priemer cez seedy 0–2.", "",
        "Modely: " + ", ".join(f"{k} = `{v.as_posix()}`" for k, v in runs.items()), "",
        "## Súhrn (priemer cez seedy)", "", md_table(agg.reset_index()), "",
        "## Podľa rodiny (seed 0)", "", md_table(fdf), "",
    ]
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
