"""Doplnok k súhrnu V2: krivka rozpočtu emulácie kaskád B (docs/09, bod 4) – časový test a priemer cez rodiny.

Čísla sa iba čítajú z uložených metrics.json (kaskády B); nič sa nepočíta nanovo ani nenastavuje podľa testu.
Kritérium tézy 2 (FPR < statický aj dynamický, TPR ≥ statický − 1 p. b.) sa vyhodnotí aj pre body krivky
s referenciami zo súhrnu (`comparison/v2/temporal_test.csv`, `zero_day_per_family.csv`).

    .venv\\Scripts\\python.exe -m src.evaluation.v2_budget --root runs_v2
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

VARIANTS = ["b_main", "b_direct", "b_heavy", "b_baselines", "b_nokd", "b_twobranch"]
TOL = 0.01


def latest(d: Path) -> Path | None:
    runs = sorted(p for p in d.glob("*/metrics.json"))
    return runs[-1] if runs else None


def rows(metrics: Path) -> list[dict]:
    m = json.loads(metrics.read_text(encoding="utf-8"))
    t = m["summary"]["test"]
    out = [{"bod": "pásmo neistoty", "emulation": t["_emulation_rate"][0],
            "tpr": t["cascade_b"]["recall_tpr"][0], "fpr": t["cascade_b"]["fpr"][0]}]
    for b in t["_budget_curve"]:
        out.append({"bod": f"rozpočet {b['budget_val']:.0%}", "emulation": b["emulation_rate"],
                    "tpr": b["recall_tpr"], "fpr": b["fpr"]})
    return out


def refs(df: pd.DataFrame, key: str) -> tuple[float, float]:
    r = df[df["kľúč"] == key]
    return float(r["tpr"].mean()), float(r["fpr"].mean())


def main(root: Path):
    out_dir = root / "comparison" / "v2"
    temporal = pd.read_csv(out_dir / "temporal_test.csv")
    zd = pd.read_csv(out_dir / "zero_day_per_family.csv")
    fams = sorted(p.name for p in (root / "lofo").iterdir() if p.is_dir())
    recs = []
    for v in VARIANTS:
        f = latest(root / "full" / "cascade" / v)
        if f:
            recs += [{"test": "časový", "variant": v, **r} for r in rows(f)]
        per = []
        for fam in fams:
            f = latest(root / "lofo" / fam / "cascade" / v)
            if f:
                per.append(pd.DataFrame(rows(f)).assign(rodina=fam))
        if len(per) == len(fams):
            agg = pd.concat(per).groupby("bod", sort=False)[["emulation", "tpr", "fpr"]].mean().reset_index()
            recs += [{"test": "zero-day (priemer cez rodiny)", "variant": v, **r} for r in agg.to_dict("records")]
    df = pd.DataFrame(recs)

    ref = {"časový": (refs(temporal, "static/lightgbm"), refs(temporal, "dynamic/lightgbm")),
           "zero-day (priemer cez rodiny)": (refs(zd, "static/lightgbm"), refs(zd, "dynamic/lightgbm"))}

    def ok(r):
        (ts, fs), (_, fd) = ref[r["test"]]
        return "áno" if (r["fpr"] < fs and r["fpr"] < fd and r["tpr"] >= ts - TOL) else "nie"
    df["téza 2"] = df.apply(ok, axis=1)
    df.to_csv(out_dir / "budget_curve.csv", index=False)

    lines = ["# V2 – krivka rozpočtu emulácie kaskád B (doplnok)", "",
             "> Generované `src/evaluation/v2_budget.py`. Hlavný pracovný bod = pásmo neistoty (docs/09); rozpočty 10–40 %",
             "> sú doplnková krivka – hranica sa určí na validácii, na teste je podiel emulovaných súborov vyšší (časový posun).",
             "> Stĺpec „téza 2“ = kritérium z docs/09 (FPR < statický aj dynamický LightGBM, TPR ≥ statický − 1 p. b.).", ""]
    for test, g in df.groupby("test", sort=False):
        (ts, fs), (td, fd) = ref[test]
        lines += [f"## {test}", f"Referencia: statický LightGBM TPR {ts:.4f}, FPR {fs:.4f}; dynamický LightGBM FPR {fd:.4f}.", "",
                  "| variant | bod | emulované súbory | TPR | FPR | téza 2 |", "|---|---|---|---|---|---|"]
        for r in g.itertuples():
            lines.append(f"| {r.variant} | {r.bod} | {r.emulation:.4f} | {r.tpr:.4f} | {r.fpr:.4f} | {r._7} |")
        lines.append("")
    (out_dir / "BUDGET.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Krivka rozpočtu: {out_dir / 'BUDGET.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("runs_v2"))
    main(ap.parse_args().root)
