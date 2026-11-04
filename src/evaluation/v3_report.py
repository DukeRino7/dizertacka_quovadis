r"""Súhrn V3 – B (docs/12): kaskáda so špecialistom v časovom teste a v zero-day + vyhodnotenie kritérií B1–B3.

Číta posledné behy `runs_v3/{full,lofo/<rodina>}/cascade/v3_*/` (src/cascade/specialist.py). Referencie (statický,
dynamický, hybrid LightGBM, B-baselines pri rovnakom rozpočte) sú vyhodnotené v tých istých behoch na rovnakých dátach.

    .venv\Scripts\python.exe -m src.evaluation.v3_report --root runs_v3
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

VARIANTS = {"v3_spec": "špecialista (hybrid) – HLAVNÝ", "v3_spec_dyn": "špecialista (iba dynamika)",
            "v3_spec_f10": "špecialista, tréning 10 % (citlivosť)", "v3_spec_f40": "špecialista, tréning 40 % (citlivosť)"}
REFS = {"static_only": "statický LightGBM", "dynamic_only": "dynamický LightGBM", "hybrid_only": "hybrid LightGBM",
        "b_baselines": "kaskáda B-baselines (rovnaký rozpočet, V2)"}
TOL = 0.01


def latest(d: Path) -> dict | None:
    runs = sorted(d.glob("*/metrics.json"))
    return json.loads(runs[-1].read_text(encoding="utf-8")) if runs else None


def rows_for(m: dict, setting: str, budget: str | None = None) -> list[dict]:
    b = budget or str(m["config"]["main_budget"])
    S = m["summary"][b]
    out = []
    for key, label in [("spec", VARIANTS[m["config"]["name"]])] + list(REFS.items()):
        a = S["test"]["approaches"][key]
        r = {"setting": setting, "variant": m["config"]["name"], "key": key if key != "spec" else m["config"]["name"],
             "prístup": label, "budget": float(b), "emulation": S["test"]["emulation_rate"][0] if key in ("spec", "b_baselines") else
             (0.0 if key == "static_only" else 1.0),
             "tpr": a["recall_tpr"][0], "fpr": a["fpr"][0], "f1": a["f1"][0],
             "tpr_family": a["tpr_family"][0] if a.get("tpr_family") else np.nan,
             "tpr_jan": S["holdout"]["approaches"][key]["recall_tpr"][0] if "holdout" in S else np.nan}
        if key == "spec" and m.get("costs"):
            r["cpu_ms"] = m["costs"]["cascade_cpu_ms_batch"]
        out.append(r)
    return out


def collect(root: Path) -> pd.DataFrame:
    recs = []
    for v in VARIANTS:
        m = latest(root / "full" / "cascade" / v)
        if m:
            recs += rows_for(m, "časový")
        for fam_dir in sorted((root / "lofo").glob("*")) if (root / "lofo").exists() else []:
            m = latest(fam_dir / "cascade" / v)
            if m:
                recs += rows_for(m, fam_dir.name)
    return pd.DataFrame(recs)


def curve(root: Path) -> pd.DataFrame:
    recs = []
    for v in VARIANTS:
        for setting, d in [("časový", root / "full")] + [(p.name, p) for p in sorted((root / "lofo").glob("*"))]:
            m = latest(d / "cascade" / v)
            if not m:
                continue
            for b in m["summary"]:
                for r in rows_for(m, setting, b):
                    if r["key"] in (v, "b_baselines"):
                        recs.append(r)
    return pd.DataFrame(recs)


def fmt(v, d=4):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] +
                     ["| " + " | ".join(fmt(x) if isinstance(x, float) else str(x) for x in r) + " |" for r in df.itertuples(index=False)])


def main(root: Path):
    out = root / "comparison" / "v3"
    out.mkdir(parents=True, exist_ok=True)
    df = collect(root)
    if df.empty:
        raise SystemExit("žiadne behy V3")
    df.to_csv(out / "specialist_main_budget.csv", index=False)
    cv = curve(root)
    cv.to_csv(out / "specialist_budget_curve.csv", index=False)
    L = ["# V3 – B: kaskáda so špecialistom (súhrn)", "",
         "> Generované `src/evaluation/v3_report.py`. Plán a kritériá (určené vopred): `docs/12_plan_v3.md`.",
         "> Hlavný bod = rozpočet emulácie 10 % (hranica z validácie). Prahy z validácie, priemer cez seedy.",
         "> Referencie sú z tých istých behov (rovnaké dáta). Zero-day = priemer cez vynechané rodiny.", ""]

    # 1) časový test
    t = df[df.setting == "časový"].drop_duplicates("key")
    if len(t):
        L += ["## 1. Časový test (rozdelenie V1)", "",
              md(t[["prístup", "tpr", "fpr", "f1", "emulation"] + (["cpu_ms"] if "cpu_ms" in t else [])]), ""]

    # 2) zero-day
    z = df[df.setting != "časový"].drop_duplicates(["setting", "key"])
    fams = sorted(z.setting.unique())
    if len(z):
        agg = z.groupby(["key", "prístup"], sort=False).agg(
            tpr_family=("tpr_family", "mean"), sd=("tpr_family", "std"), worst=("tpr_family", "min"),
            tpr_jan=("tpr_jan", "mean"), fpr=("fpr", "mean"), tpr=("tpr", "mean"), emulation=("emulation", "mean"),
            n=("setting", "nunique")).reset_index()
        L += [f"## 2. Zero-day – priemer cez {len(fams)} rodín ({', '.join(fams)})", "",
              md(agg.drop(columns="key").rename(columns={"tpr_family": "TPR vynech. rodiny", "sd": "sm. odch.",
                                                         "worst": "najhoršia", "tpr_jan": "TPR január", "tpr": "TPR všetok malvér",
                                                         "emulation": "emulované", "n": "rodín"})), "",
              "### TPR vynechanej rodiny podľa rodiny (test)", "",
              md(z.pivot_table(index="prístup", columns="setting", values="tpr_family", sort=False).reset_index()), ""]

        # 3) kritériá
        def zz(key):
            return z[z.key == key].set_index("setting")
        L += ["## 3. Kritériá (docs/12, bod 2)", ""]
        for v in ("v3_spec", "v3_spec_dyn", "v3_spec_f10", "v3_spec_f40"):
            if v not in set(z.key):
                continue
            sp, st, dy, bb = zz(v), zz("static_only"), zz("dynamic_only"), zz("b_baselines")
            common = sp.index.intersection(st.index)
            better = int((sp.loc[common, "tpr_family"] >= st.loc[common, "tpr_family"]).sum())
            b1 = (sp.tpr_family.mean() >= st.tpr_family.mean() + TOL) and (sp.fpr.mean() <= st.fpr.mean()) and better >= 5
            b3 = (sp.tpr_family.mean() >= bb.tpr_family.mean() + TOL) and (sp.fpr.mean() <= bb.fpr.mean() + 0.001)

            def b2(spf, stf, dyf):
                return (spf.fpr.mean() < stf.fpr.mean()) and (spf.fpr.mean() < dyf.fpr.mean()) and (spf.tpr.mean() >= stf.tpr.mean() - TOL)
            b2z = b2(sp, st, dy)
            tt = df[df.setting == "časový"].set_index("key")
            b2t = b2(tt.loc[[v]], tt.loc[["static_only"]], tt.loc[["dynamic_only"]]) if v in tt.index else None
            sens = " _(citlivosť, nie hlavný variant)_" if v.endswith(("f10", "f40")) else ""
            L += [f"### {VARIANTS[v]}{sens}",
                  f"- **B1 (téza 1):** TPR vynech. rodiny {sp.tpr_family.mean():.4f} vs. statický {st.tpr_family.mean():.4f} "
                  f"(potrebné +{TOL:.0%}), FPR {sp.fpr.mean():.4f} vs. {st.fpr.mean():.4f}, lepší alebo rovný v {better} z {len(common)} rodín "
                  f"→ **{'splnené' if b1 else 'nesplnené'}**",
                  f"- **B2 (téza 2):** zero-day FPR {sp.fpr.mean():.4f} (statický {st.fpr.mean():.4f}, dynamický {dy.fpr.mean():.4f}), "
                  f"TPR {sp.tpr.mean():.4f} vs. statický {st.tpr.mean():.4f} → **{'splnené' if b2z else 'nesplnené'}**; časový test → "
                  f"**{'–' if b2t is None else ('splnené' if b2t else 'nesplnené')}**",
                  f"- **B3 (prínos oproti V2):** TPR vynech. rodiny {sp.tpr_family.mean():.4f} vs. B-baselines {bb.tpr_family.mean():.4f}, "
                  f"FPR {sp.fpr.mean():.4f} vs. {bb.fpr.mean():.4f} → **{'splnené' if b3 else 'nesplnené'}**", ""]

    # 4) krivka rozpočtu
    if len(cv):
        c = cv.groupby(["variant", "key", "budget", cv.setting.eq("časový").map({True: "časový", False: "zero-day"})],
                       sort=False)[["emulation", "tpr", "fpr", "tpr_family"]].mean().reset_index()
        c.columns = ["variant", "prístup", "rozpočet", "test", "emulované", "TPR", "FPR", "TPR vynech. rodiny"]
        L += ["## 4. Krivka rozpočtu emulácie (doplnok)", "", md(c), ""]
    (out / "README.md").write_text("\n".join(L), encoding="utf-8")
    print(f"Súhrn V3 (B): {out / 'README.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("runs_v3"))
    main(ap.parse_args().root)
