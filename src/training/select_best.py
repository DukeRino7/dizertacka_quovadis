r"""Výber najlepšieho modelu skupiny podľa dohodnutého pravidla (docs/00_vyskumne_otazky.md, configs/selection.yaml).

Pravidlo (iba validácia): najvyššie TPR pri FPR 1 %; kandidáti, ktorých rozdiel od najlepšieho je menší ako
smerodajná odchýlka cez seedy, sú „zhodní“ → z nich najvyššie ROC-AUC; ak aj tu rozdiel < sm. odchýlka →
najnižší CPU čas na vzorku (benchmark). Výsledok: runs/selection/<skupina>.json (+ .md) – číta ho 'auto:<skupina>'.

    .venv\Scripts\python.exe -m src.training.select_best --groups hybrid static dynamic
"""
import argparse
import json

import pandas as pd

from src.common.config import load_config
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import git_info, now_iso, write_json


def _latest(spec: str):
    base = RUNS_DIR / spec
    runs = sorted(r for r in base.iterdir() if (r / "metrics.json").exists()) if base.exists() else []
    return runs[-1] if runs else None


def candidates(specs: list[str], rule: dict) -> pd.DataFrame:
    rows = []
    for spec in specs:
        run = _latest(spec)
        if run is None:
            rows.append({"spec": spec, "run": None})
            continue
        S = json.loads((run / "metrics.json").read_text(encoding="utf-8"))["summary"][rule["split"]]
        b = run / "benchmark.json"
        cpu = json.loads(b.read_text(encoding="utf-8"))["cpu_batch"]["cpu_ms_per_sample"] if b.exists() else None
        rows.append({"spec": spec, "run": rel(run),
                     "primary": S[rule["primary"]]["mean"], "primary_std": S[rule["primary"]]["std"],
                     "secondary": S[rule["secondary"]]["mean"], "secondary_std": S[rule["secondary"]]["std"],
                     "cpu_ms_batch": cpu})
    return pd.DataFrame(rows)


def _within(d: pd.DataFrame, col: str) -> pd.DataFrame:
    """Kandidáti, ktorých rozdiel od najlepšieho v stĺpci col je <= väčšia z ich smerodajných odchýlok."""
    best = d.iloc[0]
    tol = d[f"{col}_std"].where(d[f"{col}_std"] > best[f"{col}_std"], best[f"{col}_std"])
    return d[(best[col] - d[col]) <= tol]


def select(df: pd.DataFrame) -> tuple[str, list[str]]:
    d = df.dropna(subset=["run"]).sort_values("primary", ascending=False).reset_index(drop=True)
    if d.empty:
        raise SystemExit("žiadny kandidát nemá dokončený beh")
    tied = _within(d, "primary")
    steps = [f"1) najvyššie TPR@FPR1%: {d.iloc[0]['spec']} ({d.iloc[0]['primary']:.5f}); "
             f"zhodní v rámci sm. odchýlky: {list(tied['spec'])}"]
    if len(tied) > 1:
        tied = tied.sort_values("secondary", ascending=False).reset_index(drop=True)
        steps.append(f"2) najvyššie ROC-AUC: {tied.iloc[0]['spec']} ({tied.iloc[0]['secondary']:.5f})")
        tied = _within(tied, "secondary")
        steps[-1] += f"; zhodní: {list(tied['spec'])}"
        if len(tied) > 1 and tied["cpu_ms_batch"].notna().all():
            tied = tied.sort_values("cpu_ms_batch")
            steps.append(f"3) najnižší CPU čas na vzorku: {tied.iloc[0]['spec']} ({tied.iloc[0]['cpu_ms_batch']:.4f} ms)")
        elif len(tied) > 1:
            steps.append("3) CPU čas chýba pre niektorého zhodného kandidáta – rozhoduje poradie podľa ROC-AUC")
    return str(tied.iloc[0]["spec"]), steps


def main(groups: list[str]):
    cfg = load_config("configs/selection.yaml")
    out = RUNS_DIR / "selection"
    out.mkdir(parents=True, exist_ok=True)
    for g in groups:
        df = candidates(cfg["groups"][g], cfg["rule"])
        chosen, steps = select(df)
        missing = df.loc[df["run"].isna(), "spec"].tolist()
        write_json({"created": now_iso(), "group": g, "chosen": chosen,
                    "chosen_run": df.loc[df["spec"] == chosen, "run"].iloc[0], "rule": cfg["rule"], "steps": steps,
                    "missing_candidates": missing, "candidates": df.to_dict("records"), "git": git_info()},
                   out / f"{g}.json")
        lines = "\n".join("- " + s for s in steps)
        (out / f"{g}.md").write_text(
            f"# Výber: {g}\n\n> Generované `src/training/select_best.py` ({now_iso()}). Pravidlo: `configs/selection.yaml`, "
            f"`docs/00_vyskumne_otazky.md`.\n\n**Vybraný: `{chosen}`**\n\nPostup:\n{lines}\n\n"
            f"Chýbajúci kandidáti: {missing or 'žiadni'}\n\n"
            "primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)\n\n"
            f"```\n{df.to_string(index=False)}\n```\n", encoding="utf-8")
        print(f"{g}: vybraný {chosen}")


def resolve_auto(spec: str) -> str:
    """'auto:<skupina>' -> vybraný '<prístup>/<model>' z runs/selection/<skupina>.json."""
    if not spec.startswith("auto:"):
        return spec
    p = RUNS_DIR / "selection" / f"{spec[5:]}.json"
    if not p.exists():
        raise FileNotFoundError(f"{spec}: chýba {p} – najprv spustiť src.training.select_best")
    return json.loads(p.read_text(encoding="utf-8"))["chosen"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", nargs="*", default=["hybrid", "static", "dynamic"])
    main(ap.parse_args().groups)
