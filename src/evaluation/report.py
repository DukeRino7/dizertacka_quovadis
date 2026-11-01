"""Generovanie README.md pre beh a súhrnného CLAUDE.md pre model (runs/<prístup>/<model>/)."""
import json
from pathlib import Path

import pandas as pd

from src.common.paths import rel

SPLIT_SK = {"train": "train (podvzorka)", "validation": "validácia", "test": "test"}
ROWS = [("roc_auc", "ROC-AUC"), ("pr_auc", "PR-AUC"), ("tpr_at_fpr_0.01", "TPR pri FPR 1 %"),
        ("tpr_at_fpr_0.001", "TPR pri FPR 0,1 %"), ("log_loss", "log loss"), ("brier", "Brier skóre")]
THR_ROWS = [("accuracy", "accuracy"), ("balanced_accuracy", "balanced accuracy"), ("precision", "precision"),
            ("recall_tpr", "recall (TPR)"), ("fpr", "FPR"), ("f1", "F1"), ("mcc", "MCC")]


def _ms(d, key, digits=4):
    v = d[key]
    return f"{v['mean']:.{digits}f} ± {v['std']:.{digits}f}"


def _metric_table(summary, rows, prefix=""):
    lines = ["| metrika | " + " | ".join(SPLIT_SK[s] for s in summary) + " |", "|---|" + "---|" * len(summary)]
    for key, label in rows:
        lines.append(f"| {label} | " + " | ".join(_ms(summary[s], prefix + key) for s in summary) + " |")
    return "\n".join(lines)


def write_run_readme(run: Path, cfg, protocol, metrics, timing, trials: pd.DataFrame) -> None:
    S = metrics["summary"]
    seeds = metrics["seeds"]
    gap = S["train"]["roc_auc"]["mean"] - S["validation"]["roc_auc"]["mean"]
    t = timing
    gpu = ""
    if "gpu_latency" in t:
        gpu = (f"| GPU latencia (batch 1) | {t['gpu_latency']['median_ms']:.3f} ms (p95 {t['gpu_latency']['p95_ms']:.3f}) |\n"
               f"| GPU priepustnosť | {t['gpu_throughput']['samples_per_s']:,.0f} vzoriek/s |\n"
               f"| GPU špičková pamäť | {t['gpu_peak_memory_mb']:.0f} MB |\n").replace(",", " ")
    trans = ""
    if "transform_cpu_latency" in t:
        trans = (f"| transformácia vstupu – latencia (1 vlákno) | {t['transform_cpu_latency']['median_ms']:.3f} ms |\n"
                 f"| transformácia vstupu – priepustnosť | {t['transform_cpu_throughput']['samples_per_s']:,.0f} vzoriek/s |\n").replace(",", " ")
    text = _build(run, cfg, protocol, metrics, timing, S, seeds, gap, gpu, trans)
    (run / "README.md").write_text(text, encoding="utf-8")


def _build(run, cfg, protocol, metrics, t, S, seeds, gap, gpu, trans):
    n_par = f"{t['n_parameters']:,}".replace(",", " ")
    thr = f"{t['cpu_throughput']['samples_per_s']:,.0f}".replace(",", " ")
    lc = "![učenie](plots/learning_curve.png)" if (run / "plots" / "learning_curve.png").exists() else ""
    return f"""# {cfg['approach']}/{cfg['name']} – beh `{run.name}`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `{cfg['model']}` – {cfg.get('description', '')}
- **Ladenie:** {t['hpo_trials_completed']} dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, {t['hpo_s'] / 60:.1f} min
- **Finálne modely:** seedy {seeds}; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{json.dumps(metrics['best_params'], ensure_ascii=False)}`

## Detekčná kvalita (bez prahu)
{_metric_table(S, ROWS)}

Rozdiel ROC-AUC train − validácia: **{gap:.4f}** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ {protocol['thresholds']['target_fpr']:.0%} na validácii)
{_metric_table(S, THR_ROWS, 'at_val_fpr.')}

## Pri pevnom prahu {protocol['thresholds']['fixed']}
{_metric_table(S, THR_ROWS, 'at_fixed.')}

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | {sum(t['fit_s_per_seed']) / len(t['fit_s_per_seed']):.1f} s (priemer cez seedy) |
| ladenie spolu | {t['hpo_s']:.0f} s |
| počet parametrov / uzlov | {n_par} |
| veľkosť modelu na disku | {t['model_disk_bytes'] / 1e6:.2f} MB |
{trans}| CPU latencia modelu (batch 1, {protocol['timing']['latency_threads']} vlákno) | {t['cpu_latency']['median_ms']:.3f} ms (p95 {t['cpu_latency']['p95_ms']:.3f}) |
| CPU priepustnosť ({protocol['timing']['throughput_threads']} vlákien) | {thr} vzoriek/s |
{gpu}
## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
| ![ladenie](plots/hpo_history.png) | {lc} |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
"""


def update_model_index(model_dir: Path) -> None:
    """Prehľad všetkých behov modelu v runs/<prístup>/<model>/CLAUDE.md."""
    rows = []
    for run in sorted(p for p in model_dir.iterdir() if p.is_dir() and (p / "metrics.json").exists()):
        m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
        tm = json.loads((run / "timing.json").read_text(encoding="utf-8"))
        S = m["summary"]
        rows.append(f"| [`{run.name}`]({run.name}/README.md) | {S['validation']['roc_auc']['mean']:.4f} | "
                    f"{S['test']['roc_auc']['mean']:.4f} ± {S['test']['roc_auc']['std']:.4f} | "
                    f"{S['test']['tpr_at_fpr_0.01']['mean']:.4f} | {S['test']['at_val_fpr.f1']['mean']:.4f} | "
                    f"{tm['cpu_latency']['median_ms']:.3f} | {tm['model_disk_bytes'] / 1e6:.2f} |")
    text = f"""# {rel(model_dir)}/

Behy modelu (generované automaticky po každom behu). Detail behu v jeho `README.md`.

| beh | ROC-AUC val | ROC-AUC test | TPR@FPR1% test | F1 test (prah z val) | CPU latencia [ms] | veľkosť [MB] |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"
    (model_dir / "CLAUDE.md").write_text(text, encoding="utf-8")
