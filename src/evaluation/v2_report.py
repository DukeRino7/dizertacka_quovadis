"""Súhrn V2 (docs/09): zero-day (vynechanie rodiny) a časový test, vyhodnotenie téz podľa kritérií určených vopred.

Číta iba uložené výstupy:
- časový test: modely a kaskády A z V1 (`--v1`, napr. runs_final), nové modely a kaskády B z `<root>/full`,
- zero-day: `<root>/lofo/<rodina>/` (modely, kaskády A aj B).
Hodnoty pri prahoch z validácie (FPR ≤ 1 %), priemer cez seedy; pri zero-day potom priemer a sm. odchýlka cez rodiny.

    .venv\\Scripts\\python.exe -m src.evaluation.v2_report --root runs_v2 --v1 runs_final
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.paths import PROJECT_ROOT, rel
from src.common.provenance import now_iso

TOL = 0.01   # tolerancia 1 p. b. (docs/09, tézy 2 a 3)

MODELS = {   # hlavné modely (architektúry podľa výberu V1)
    "static/lightgbm": "statický LightGBM",
    "dynamic/lightgbm": "dynamický LightGBM",
    "hybrid/lightgbm": "hybrid LightGBM",
    "hybrid/two_branch": "hybrid dvojvetvová sieť (komplexný)",
    "students_static/mlp_kd": "študent statický (KD z hybridu)",
    "students_static/mlp_nokd": "študent statický (bez KD)",
    "students_static/mlp_kd_modal": "študent statický (KD, variant A)",
    "students_static/mlp_kd_twobranch": "študent statický (KD z dvojvetvovej siete)",
    "students_dynamic/mlp_kd": "študent dynamický (KD z hybridu)",
    "students_dynamic/mlp_nokd": "študent dynamický (bez KD)",
    "students_dynamic/mlp_kd_modal": "študent dynamický (KD, variant A)",
    "students_dynamic/mlp_kd_twobranch": "študent dynamický (KD z dvojvetvovej siete)",
}
LADDER = [f"{a}/{m}" for a in ("static", "dynamic", "hybrid") for m in ("lr", "rf", "lightgbm", "mlp_small", "mlp_large")] + \
    ["dynamic/seq_cnn", "hybrid/two_branch"]
CASC_A = {"main": "kaskáda A-main", "nokd": "kaskáda A-nokd", "modal": "kaskáda A-modal", "heavy": "kaskáda A-heavy",
          "baselines": "kaskáda A-baselines", "twobranch": "kaskáda A-twobranch"}
CASC_B = {"b_main": "kaskáda B-main", "b_direct": "kaskáda B-direct", "b_heavy": "kaskáda B-heavy",
          "b_baselines": "kaskáda B-baselines", "b_nokd": "kaskáda B-nokd", "b_twobranch": "kaskáda B-twobranch"}


def latest(base: Path) -> Path | None:
    runs = sorted(r for r in base.iterdir() if (r / "metrics.json").exists()) if base.exists() else []
    return runs[-1] if runs else None


def load(p: Path) -> dict:
    return json.loads((p / "metrics.json").read_text(encoding="utf-8"))


def find(roots: list[Path], sub: str) -> Path | None:
    for r in roots:
        x = latest(r / sub)
        if x:
            return x
    return None


def cpu(run: Path | None) -> float | None:
    b = run / "benchmark.json" if run else None
    return json.loads(b.read_text(encoding="utf-8"))["cpu_batch"]["cpu_ms_per_sample"] if b and b.exists() else None


# ----------------------------------------------------------------------------- metriky jedného behu

def model_row(run: Path, fam: str | None) -> dict:
    m = load(run)
    rows = []
    for p in m["per_seed"]:
        t = p["test"]["at_val_fpr"]
        pf = {x["family"]: x["detected_rate"] for x in t["per_family"]}
        rows.append({"tpr": t["recall_tpr"], "fpr": t["fpr"], "f1": t["f1"],
                     "tpr_fam": pf.get(fam) if fam else None,
                     "tpr_jan": p.get("holdout", {}).get("tpr_at_val_fpr")})
    return pd.DataFrame(rows).mean(numeric_only=True).to_dict()


def cascade_row(run: Path, fam: str | None, kind: str) -> dict:
    m = load(run)
    key = "cascade" if kind == "A" else "cascade_b"
    rows = []
    for p in m["per_seed"]:
        a = p["test"]["approaches"][key]
        pf = {x["family"]: 1 - x["error_rate"] for x in p["test"]["cascade"]["per_family"]}
        if kind == "A":
            jan = p.get("holdout", {}).get("tpr", {}).get("cascade")
            emu = 1.0                                     # kaskáda A emuluje každý súbor
        else:
            jan = p["holdout"]["approaches"]["cascade_b"]["recall_tpr"] if "holdout" in p else None
            emu = p["test"]["cascade"]["emulation_rate"]
        rows.append({"tpr": a["recall_tpr"], "fpr": a["fpr"], "f1": a["f1"], "tpr_fam": pf.get(fam) if fam else None,
                     "tpr_jan": jan, "emulation": emu})
    out = pd.DataFrame(rows).mean(numeric_only=True).to_dict()
    costs = m.get("costs") or []
    lab = "kaskáda (odhad)" if kind == "A" else "kaskáda B (odhad)"
    out["cpu_ms"] = next((c[lab] for c in costs if c["meranie"].startswith("CPU čas ms/vz. (dávka)")), None)
    return out


# ----------------------------------------------------------------------------- zber

def collect_temporal(root: Path, v1: Path) -> pd.DataFrame:
    full = root / "full"
    rows = []
    for spec, lab in MODELS.items():
        run = find([full, v1], spec)
        if run:
            rows.append({"prístup": lab, "kľúč": spec, **model_row(run, None), "emulation": 1.0 if not spec.startswith(("static", "students_static")) else 0.0,
                         "cpu_ms": cpu(run)})
    for name, lab in CASC_A.items():
        run = find([full, v1], f"cascade/{name}")
        if run:
            rows.append({"prístup": lab, "kľúč": f"cascade/{name}", **cascade_row(run, None, "A")})
    for name, lab in CASC_B.items():
        run = find([full], f"cascade/{name}")
        if run:
            rows.append({"prístup": lab, "kľúč": f"cascade/{name}", **cascade_row(run, None, "B")})
    return pd.DataFrame(rows)


def collect_zero_day(root: Path) -> pd.DataFrame:
    rows = []
    lofo = root / "lofo"
    for fdir in sorted(d for d in lofo.iterdir() if d.is_dir()) if lofo.exists() else []:
        fam = fdir.name
        for spec in list(MODELS) + [s for s in LADDER if s not in MODELS]:
            run = latest(fdir / spec)
            if run:
                rows.append({"rodina": fam, "kľúč": spec, "prístup": MODELS.get(spec, spec), **model_row(run, fam)})
        for kind, table in (("A", CASC_A), ("B", CASC_B)):
            for name, lab in table.items():
                run = latest(fdir / "cascade" / name)
                if run:
                    rows.append({"rodina": fam, "kľúč": f"cascade/{name}", "prístup": lab, **cascade_row(run, fam, kind)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- tézy

def verdict_t2(df: pd.DataFrame, cascades: list[str]) -> list[dict]:
    """Téza 2: FPR kaskády < FPR statického aj dynamického a TPR ≥ TPR statického − 1 p. b."""
    if df.empty:
        return []
    g = df.set_index("kľúč")
    if not {"static/lightgbm", "dynamic/lightgbm"} <= set(g.index):
        return []
    s, d = g.loc["static/lightgbm"], g.loc["dynamic/lightgbm"]
    out = []
    for c in cascades:
        if c in g.index:
            x = g.loc[c]
            ok_fpr = x["fpr"] < s["fpr"] and x["fpr"] < d["fpr"]
            ok_tpr = x["tpr"] >= s["tpr"] - TOL
            out.append({"kaskáda": x["prístup"], "FPR": x["fpr"], "FPR statický": s["fpr"], "FPR dynamický": d["fpr"],
                        "TPR": x["tpr"], "TPR statický": s["tpr"], "spĺňa": "áno" if ok_fpr and ok_tpr else "nie"})
    return out


def fmt(v, p=4):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else (f"{v:.{p}f}" if isinstance(v, float) else str(v))


def table(df: pd.DataFrame, cols: dict) -> str:
    if df is None or len(df) == 0:
        return "_žiadne dáta_"
    lines = ["| " + " | ".join(cols.values()) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(fmt(r.get(c)) for c in cols) + " |")
    return "\n".join(lines)


def main(root: str, v1: str) -> Path:
    R, V1 = PROJECT_ROOT / root, PROJECT_ROOT / v1
    out = R / "comparison" / "v2"
    out.mkdir(parents=True, exist_ok=True)
    T = collect_temporal(R, V1)
    Z = collect_zero_day(R)
    T.to_csv(out / "temporal_test.csv", index=False)
    Z.to_csv(out / "zero_day_per_family.csv", index=False)
    fams = sorted(Z["rodina"].unique()) if len(Z) else []

    # zero-day: priemer a sm. odchýlka cez rodiny
    if len(Z):
        agg = Z.groupby(["kľúč", "prístup"], sort=False).agg(
            tpr_fam=("tpr_fam", "mean"), tpr_fam_std=("tpr_fam", "std"), tpr_fam_min=("tpr_fam", "min"),
            tpr_jan=("tpr_jan", "mean"), fpr=("fpr", "mean"), fpr_std=("fpr", "std"), tpr=("tpr", "mean"),
            f1=("f1", "mean"), emulation=("emulation", "mean"), n=("rodina", "nunique")).reset_index()
        piv = Z.pivot_table(index="prístup", columns="rodina", values="tpr_fam", sort=False).reset_index()
    else:
        agg, piv = pd.DataFrame(), pd.DataFrame()
    main_keys = list(MODELS) + [f"cascade/{k}" for k in list(CASC_A) + list(CASC_B)]
    aggm = agg[agg["kľúč"].isin(main_keys)] if len(agg) else agg
    aggl = agg[agg["kľúč"].isin(LADDER)] if len(agg) else agg

    # téza 1: kaskády vs. samostatné modely v zero-day
    t1 = ""
    if len(agg):
        g = agg.set_index("kľúč")
        ref = [k for k in ("static/lightgbm", "dynamic/lightgbm", "hybrid/lightgbm", "hybrid/two_branch") if k in g.index]
        lines = []
        for c in ("cascade/main", "cascade/b_main"):
            if c not in g.index:
                continue
            for k in ref:
                wins = int((Z[Z["kľúč"] == c].set_index("rodina")["tpr_fam"] >= Z[Z["kľúč"] == k].set_index("rodina")["tpr_fam"]).sum())
                lines.append(f"- {g.loc[c, 'prístup']} vs. {g.loc[k, 'prístup']}: TPR vynechanej rodiny "
                             f"{g.loc[c, 'tpr_fam']:.4f} ± {fmt(g.loc[c, 'tpr_fam_std'])} vs. {g.loc[k, 'tpr_fam']:.4f} ± "
                             f"{fmt(g.loc[k, 'tpr_fam_std'])}; FPR {g.loc[c, 'fpr']:.4f} vs. {g.loc[k, 'fpr']:.4f}; "
                             f"kaskáda ≥ model v {wins} z {len(fams)} rodín")
        t1 = "\n".join(lines)

    casc_keys = [f"cascade/{k}" for k in list(CASC_A) + list(CASC_B)]
    t2_time = verdict_t2(T, casc_keys)
    t2_zero = verdict_t2(agg.rename(columns={}) if len(agg) else agg, casc_keys)

    # téza 3: študenti vs. komplexný hybrid (TPR vynechanej rodiny, CPU z časového testu)
    t3 = []
    if len(agg):
        g = agg.set_index("kľúč")
        cpu_t = T.set_index("kľúč")["cpu_ms"] if len(T) else pd.Series(dtype=float)
        for ref in ("hybrid/two_branch", "hybrid/lightgbm"):
            for s in [k for k in MODELS if k.startswith("students_")]:
                if ref in g.index and s in g.index:
                    d = g.loc[s, "tpr_fam"] - g.loc[ref, "tpr_fam"]
                    cs, cr = cpu_t.get(s), cpu_t.get(ref)
                    t3.append({"študent": MODELS[s], "referencia": MODELS[ref], "TPR vynech. rodiny študent": g.loc[s, "tpr_fam"],
                               "TPR referencia": g.loc[ref, "tpr_fam"], "rozdiel": d,
                               "CPU ms študent": cs, "CPU ms referencia": cr,
                               "rýchlejší": "–" if cs is None or cr is None else ("áno" if cs < cr else "nie"),
                               "porovnateľná presnosť (≥ −1 p. b.)": "áno" if d >= -TOL else "nie"})

    cols_t = {"prístup": "prístup", "tpr": "TPR", "fpr": "FPR", "f1": "F1", "emulation": "emulované súbory", "cpu_ms": "CPU ms/vz."}
    cols_z = {"prístup": "prístup", "tpr_fam": "TPR vynech. rodiny (test)", "tpr_fam_std": "sm. odch. cez rodiny",
              "tpr_fam_min": "najhoršia rodina", "tpr_jan": "TPR vynech. rodiny (január)", "fpr": "FPR",
              "tpr": "TPR všetok malvér", "emulation": "emulované súbory"}
    piv_cols = {"prístup": "prístup", **{f: f for f in fams}}
    t2c = {"kaskáda": "kaskáda", "FPR": "FPR", "FPR statický": "FPR statický", "FPR dynamický": "FPR dynamický",
           "TPR": "TPR", "TPR statický": "TPR statický", "spĺňa": "spĺňa kritérium"}
    text = f"""# V2 – zero-day a kaskáda B: súhrn a vyhodnotenie téz

> Generované `src/evaluation/v2_report.py` ({now_iso()}). Plán a kritériá (určené vopred): `docs/09_plan_v2.md`.
> Prahy z validácie (FPR ≤ 1 %), priemer cez seedy. Zero-day: v každom behu je jedna rodina vynechaná z tréningu aj
> validácie; hodnoty sú priemer (± sm. odchýlka) cez {len(fams)} rodín: {', '.join(fams) or '–'}.
> Hyperparametre z V1 (bez ladenia). Emulácia sa nemeria – „emulované súbory“ = podiel súborov, ktoré treba emulovať.

## 1. Časový test (rozdelenie V1, test apríl 2022)
Modely a kaskády A z `{rel(V1)}`, nové modely a kaskády B z `{rel(R / 'full')}`.

{table(T, cols_t)}

## 2. Zero-day – priemer cez rodiny (test apríl 2022 + januárové vzorky vynechanej rodiny)
{table(aggm, cols_z)}

### TPR vynechanej rodiny podľa rodiny (test)
{table(piv, piv_cols)}

### Celý rebríček modelov (doplnok)
{table(aggl, cols_z)}

## 3. Tézy (kritériá z docs/09)
### Téza 1 – kaskáda presnejšia a stabilnejšia v zero-day
{t1 or '_žiadne dáta_'}

### Téza 2 – menej falošných poplachov pri zachovaní citlivosti (TPR ≥ statický − 1 p. b.)
Časový test:

{table(pd.DataFrame(t2_time), t2c)}

Zero-day (priemer cez rodiny):

{table(pd.DataFrame(t2_zero), t2c)}

### Téza 3 – študent rýchlejší a s porovnateľnou presnosťou ako komplexný hybrid (zero-day, ±1 p. b.)
{table(pd.DataFrame(t3), {k: k for k in (t3[0].keys() if t3 else [])})}

### Téza 4 – podiel súborov, ktoré treba emulovať
Kaskáda A, dynamický a hybridný model emulujú 100 % súborov; kaskády B iba neisté (stĺpec „emulované súbory“
v tabuľkách 1 a 2). Čas s predpokladom 60 s emulácie na súbor: kaskáda B ≈ podiel × 60 s.

Súbory: `temporal_test.csv`, `zero_day_per_family.csv`.
"""
    (out / "README.md").write_text(text, encoding="utf-8")
    print(f"Súhrn V2: {rel(out)}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="runs_v2")
    ap.add_argument("--v1", default="runs_final")
    a = ap.parse_args()
    main(a.root, a.v1)
