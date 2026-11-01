"""Porovnanie kontrolných experimentov (ablácií) s pôvodným modelom.

Pre každý beh v runs/<priečinok ablácií>/<názov>/ nájde pôvodný beh (params_from_run v timing.json)
a porovná metriky na validácii aj teste.
    .venv\Scripts\python.exe -m src.evaluation.compare_ablations --dir static_ablations
"""
import argparse
import json
from pathlib import Path

from src.common.paths import PROJECT_ROOT, RUNS_DIR, rel
from src.common.provenance import now_iso
from .compare import latest_runs

METRICS = [("roc_auc", "ROC-AUC"), ("tpr_at_fpr_0.01", "TPR@FPR 1 %"), ("tpr_at_fpr_0.001", "TPR@FPR 0,1 %"),
           ("at_val_fpr.f1", "F1*"), ("at_val_fpr.fpr", "FPR*")]


def _summary(run: Path) -> dict:
    return json.loads((run / "metrics.json").read_text(encoding="utf-8"))["summary"]


def main(directory: str, runs_root: Path = RUNS_DIR):
    rows = []
    for name, run in latest_runs(directory, runs_root).items():
        t = json.loads((run / "timing.json").read_text(encoding="utf-8"))
        base = PROJECT_ROOT / t["params_from_run"] if t.get("params_from_run") else None
        if base is None or not base.exists():
            continue
        cfg_excl = json.loads((run / "model" / "feature_mask.json").read_text())["excluded"] \
            if (run / "model" / "feature_mask.json").exists() else []
        A, B = _summary(run), _summary(base)
        rows.append((name, rel(base), len(cfg_excl), A, B, run))
    out = runs_root / "comparison" / directory
    out.mkdir(parents=True, exist_ok=True)
    lines = []
    for split, sk in [("validation", "validácia"), ("test", "test")]:
        lines += [f"\n### {sk}", "| ablácia | vynechaných | " + " | ".join(f"{l} pôvodný | {l} bez | Δ" for _, l in METRICS) + " |",
                  "|---|---|" + "---|---|---|" * len(METRICS)]
        for name, base, n_ex, A, B, run in rows:
            cells = []
            for k, _ in METRICS:
                b, a = B[split][k]["mean"], A[split][k]["mean"]
                cells += [f"{b:.4f}", f"{a:.4f}", f"{a - b:+.4f}"]
            lines.append(f"| [{name}](../../{directory}/{name}/{run.name}/README.md) | {n_ex} | " + " | ".join(cells) + " |")
    text = f"""# Kontrolné experimenty – {directory}

> Generované `src/evaluation/compare_ablations.py` ({now_iso()}). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; \* = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).
{chr(10).join(lines)}
"""
    (out / "README.md").write_text(text, encoding="utf-8")
    print(f"Porovnanie ablácií: {rel(out)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="static_ablations")
    main(ap.parse_args().dir)
