"""Experiment spoločného rebríčka: ladenie na validácii -> finálne modely s viacerými seedmi -> vyhodnotenie.

Spustenie (z koreňa projektu):
    .venv\\Scripts\\python.exe -m src.training.run_tabular --config configs/static/lr.yaml

Pravidlá (configs/protocol.yaml):
- učené transformácie a model sa fitujú iba na train,
- hyperparametre, early stopping a prahy sa určujú iba na validation,
- test sa vyhodnotí až po výbere hyperparametrov a nijako neovplyvňuje rozhodnutia.
"""
import argparse
import json
import time
from pathlib import Path

import joblib
import numpy as np
import optuna
import pandas as pd

from src.common.config import load_config
from src.common.hardware import load_protocol
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import now_iso, write_json
from src.common.run import create_run_dir, save_run_context
from src.common.seed import set_seed
from src.data.providers import feature_names, load_tabular
from src.data.static_transforms import StaticPreprocessor
from src.evaluation import plots
from src.evaluation.metrics import evaluate, threshold_for_fpr
from src.evaluation.timing import measure_inference
from src.models.registry import get_model_class
from .search_space import suggest

KEY_METRICS = ["roc_auc", "pr_auc", "tpr_at_fpr_0.001", "tpr_at_fpr_0.01", "log_loss", "brier"]
THR_METRICS = ["accuracy", "balanced_accuracy", "precision", "recall_tpr", "fpr", "f1", "mcc"]


def latest_run(approach_model: str, root: Path = RUNS_DIR) -> Path:
    """'static/lightgbm' -> posledný dokončený beh v runs/static/lightgbm/."""
    runs = sorted(r for r in (root / approach_model).iterdir() if (r / "metrics.json").exists())
    if not runs:
        raise FileNotFoundError(f"žiadny dokončený beh v runs/{approach_model}")
    return runs[-1]


def load_soft_targets(dcfg: dict, train_meta: pd.DataFrame, root: Path) -> tuple[np.ndarray, Path]:
    """Mäkké označenia učiteľa zarovnané podľa SHA-256 s tréningovými riadkami."""
    if not dcfg.get("teacher"):
        raise ValueError("distillation.teacher nie je vyplnený – učiteľ sa vyberá podľa docs/00_vyskumne_otazky.md")
    base = root / "teachers" / dcfg["teacher"].replace("/", "_")
    runs = sorted(r for r in base.iterdir() if (r / "train_oof.parquet").exists()) if base.exists() else []
    if not runs:
        raise FileNotFoundError(f"chýbajú mäkké označenia učiteľa v {base} – spustiť src.training.teacher_oof")
    oof = pd.read_parquet(runs[-1] / "train_oof.parquet")
    m = train_meta[["sha256"]].merge(oof[["sha256", "p_teacher"]], on="sha256", how="left")
    if m["p_teacher"].isna().any():
        raise ValueError(f"{int(m['p_teacher'].isna().sum())} tréningových vzoriek nemá mäkké označenie učiteľa")
    return m["p_teacher"].to_numpy(np.float32), runs[-1]


def class_weights(y: np.ndarray, mode: str | None) -> np.ndarray:
    if mode != "balanced":
        return np.ones(len(y), dtype=np.float32)
    n, pos = len(y), y.sum()
    w = {0: n / (2 * (n - pos)), 1: n / (2 * pos)}
    return np.where(y == 1, w[1], w[0]).astype(np.float32)


def dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def flatten(m: dict, prefix="") -> dict:
    out = {}
    for k, v in m.items():
        if isinstance(v, dict):
            out.update(flatten(v, f"{prefix}{k}."))
        elif not isinstance(v, list):
            out[f"{prefix}{k}"] = v
    return out


# ----------------------------------------------------------------------------- ladenie

def run_hpo(model_cls, cfg, protocol, data, w, run: Path, log, soft=None) -> tuple[dict, pd.DataFrame, float]:
    hpo = protocol["hpo"]
    Xtr, ytr, _ = data["train"]; Xva, yva, _ = data["validation"]
    fixed = cfg.get("fixed_params", {}) or {}

    def objective(trial):
        params = {**fixed, **suggest(trial, cfg["search_space"])}
        set_seed(hpo["trial_seed"])
        m = model_cls(params, seed=hpo["trial_seed"], threads=protocol["training_threads"])
        m.soft_targets = soft
        t = time.perf_counter()
        info = m.fit(Xtr, ytr, w, Xva, yva)
        trial.set_user_attr("fit_s", time.perf_counter() - t)
        trial.set_user_attr("n_parameters", m.n_parameters())
        for k in ("best_iteration", "best_epoch"):
            if k in info:
                trial.set_user_attr(k, info[k])
        from sklearn.metrics import roc_auc_score
        score = roc_auc_score(yva, m.predict_proba(Xva))
        log(f"  pokus {trial.number:3d}: AUC val = {score:.5f}  ({trial.user_attrs['fit_s']:.0f} s)  {params}")
        return score

    if hpo["objective"] != "roc_auc":
        raise NotImplementedError(hpo["objective"])
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=hpo["sampler_seed"]))
    t = time.perf_counter()
    study.optimize(objective, n_trials=hpo["n_trials"], timeout=hpo["timeout_s"], catch=(RuntimeError, MemoryError, ValueError))
    hpo_s = time.perf_counter() - t
    trials = study.trials_dataframe(attrs=("number", "value", "state", "params", "user_attrs", "duration"))
    trials["state"] = trials["state"].astype(str)
    trials.to_csv(run / "hpo_trials.csv", index=False)
    best = {**fixed, **study.best_params}
    return best, trials, hpo_s


# ----------------------------------------------------------------------------- hlavný postup

def main(config_path: str, runs_root: Path | None, tag: str | None, smoke: bool) -> Path:
    cfg = load_config(config_path)
    protocol = load_protocol(cfg.get("protocol", "configs/protocol.yaml"))
    if smoke:  # rýchla kontrola, že pipeline funguje (nie je to experiment)
        protocol["hpo"]["n_trials"] = 2
        protocol["final"]["seeds"] = [0]
        protocol["timing"]["latency_samples"] = 50
        cfg.setdefault("fixed_params", {}).update(cfg.get("smoke_overrides", {}) or {})
    run = create_run_dir(cfg.get("results_approach", cfg["approach"]), cfg["name"], tag, runs_root)
    save_run_context(run, config_path, cfg, protocol)
    logf = open(run / "log.txt", "w", encoding="utf-8")

    def log(msg):
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()

    log(f"[{now_iso()}] {cfg['approach']}/{cfg['name']} -> {rel(run)}")
    model_cls = get_model_class(cfg["model"])
    timings = {}

    t = time.perf_counter()
    raw = load_tabular(cfg["approach"])
    if smoke:
        rng = np.random.default_rng(0)
        small = {}
        for s, (X, y, m) in raw.items():
            i = np.sort(rng.choice(len(y), min(5000, len(y)), replace=False))
            small[s] = (X[i], y[i], m.iloc[i].reset_index(drop=True))
        raw = small
    timings["load_data_s"] = time.perf_counter() - t

    # voliteľné vynechanie príznakov (kontrolné experimenty / ablácie)
    if cfg.get("exclude_features"):
        names = feature_names(cfg["approach"])
        missing = sorted(set(cfg["exclude_features"]) - set(names))
        if missing:
            raise ValueError(f"neznáme príznaky v exclude_features: {missing}")
        keep = np.array([n not in set(cfg["exclude_features"]) for n in names])
        raw = {s: (X[:, keep], y, m) for s, (X, y, m) in raw.items()}
        write_json({"kept_columns": np.flatnonzero(keep).tolist(), "excluded": cfg["exclude_features"]},
                   run / "model" / "feature_mask.json")
        log(f"Vynechané príznaky ({len(cfg['exclude_features'])}): {cfg['exclude_features']}")

    # učená transformácia vstupu – fit iba na tréningu
    pre = None
    data = raw
    if model_cls.needs_scaling:
        t = time.perf_counter()
        pre = StaticPreprocessor().fit(raw["train"][0])
        timings["preprocessor_fit_s"] = time.perf_counter() - t
        data = {s: (pre.transform(X), y, m) for s, (X, y, m) in raw.items()}
        joblib.dump(pre, run / "model" / "preprocessor.joblib")
        log(f"Predspracovanie: {int(pre.keep_.sum())} z {pre.n_features_in_} príznakov, signed log1p + štandardizácia")

    w = class_weights(data["train"][1], protocol.get("class_weight"))

    # destilácia vedomostí: mäkké označenia učiteľa pre tréning (out-of-fold, src/training/teacher_oof.py)
    soft = None
    if cfg.get("distillation"):
        soft, src_oof = load_soft_targets(cfg["distillation"], data["train"][2], runs_root or RUNS_DIR)
        timings["teacher_oof"] = rel(src_oof)
        log(f"Destilácia: mäkké označenia učiteľa z {rel(src_oof)}")

    if cfg.get("params_from"):
        src_run = latest_run(cfg["params_from"], runs_root or RUNS_DIR)
        best = json.loads((src_run / "metrics.json").read_text(encoding="utf-8"))["best_params"]
        trials, timings["hpo_s"] = pd.DataFrame(columns=["number", "value", "state"]), 0.0
        timings["params_from_run"] = rel(src_run)
        log(f"Bez ladenia: hyperparametre prevzaté z {rel(src_run)}")
    else:
        log(f"Ladenie: {protocol['hpo']['n_trials']} pokusov, cieľ {protocol['hpo']['objective']} na validácii")
        best, trials, timings["hpo_s"] = run_hpo(model_cls, cfg, protocol, data, w, run, log, soft)
    timings["hpo_trials_completed"] = int((trials["state"] == "COMPLETE").sum())
    log(f"Najlepšie parametre: {best}")
    plots.hpo_history(trials, run / "plots" / "hpo_history.png", f"{cfg['name']}: priebeh ladenia")

    # finálne modely
    Xtr, ytr, mtr = data["train"]; Xva, yva, mva = data["validation"]; Xte, yte, mte = data["test"]
    rng = np.random.default_rng(protocol["hpo"]["sampler_seed"])
    sub = np.sort(rng.choice(len(ytr), min(protocol["final"]["train_metrics_subsample"], len(ytr)), replace=False))
    per_seed, timing_seed0, model0 = [], None, None
    for seed in protocol["final"]["seeds"]:
        set_seed(seed)
        m = model_cls(best, seed=seed, threads=protocol["training_threads"])
        m.soft_targets = soft
        t = time.perf_counter()
        info = m.fit(Xtr, ytr, w, Xva, yva)
        fit_s = time.perf_counter() - t
        scores = {"train": m.predict_proba(Xtr[sub]), "validation": m.predict_proba(Xva), "test": m.predict_proba(Xte)}
        thr = {"fixed": protocol["thresholds"]["fixed"],
               "val_fpr": threshold_for_fpr(yva, scores["validation"], protocol["thresholds"]["target_fpr"])}
        res = {"seed": seed, "fit_s": fit_s, "n_parameters": m.n_parameters(), "thresholds": thr,
               "train_info": {k: v for k, v in info.items() if not isinstance(v, list)},
               "train": evaluate(ytr[sub], scores["train"], thr, protocol["tpr_at_fpr"]),
               "validation": evaluate(yva, scores["validation"], thr, protocol["tpr_at_fpr"], mva),
               "test": evaluate(yte, scores["test"], thr, protocol["tpr_at_fpr"], mte)}
        mdir = run / "model" / f"seed_{seed}"
        m.save(mdir)
        res["model_disk_bytes"] = dir_size(mdir) + ((run / "model" / "preprocessor.joblib").stat().st_size if pre else 0)
        for split, meta in [("validation", mva), ("test", mte)]:
            meta[["sha256", "family", "label"]].assign(score=scores[split]).to_parquet(
                run / "predictions" / f"{split}_seed{seed}.parquet", index=False)
        log(f"Seed {seed}: fit {fit_s:.1f} s | AUC train {res['train']['roc_auc']:.5f} | "
            f"val {res['validation']['roc_auc']:.5f} | test {res['test']['roc_auc']:.5f}")
        if model0 is None:
            model0, scores0, info0, res0 = m, scores, info, res
        per_seed.append(res)

    # meranie inferencie (seed 0, testovacia množina, pôvodné vstupy -> transformácia -> model)
    log("Meranie inferencie ...")
    timing = measure_inference(model0, pre.transform if pre else None, raw["test"][0], protocol["timing"])
    timing.update({"n_parameters": res0["n_parameters"], "model_disk_bytes": res0["model_disk_bytes"],
                   "fit_s_per_seed": [r["fit_s"] for r in per_seed], **timings})
    write_json(timing, run / "timing.json")

    # súhrn cez seedy
    summary = {}
    for split in ("train", "validation", "test"):
        rows = [flatten({k: r[split][k] for k in KEY_METRICS} | {f"at_{t}": {k: r[split][f"at_{t}"][k] for k in THR_METRICS}
                                                                 for t in ("fixed", "val_fpr")}) for r in per_seed]
        df = pd.DataFrame(rows)
        summary[split] = {c: {"mean": float(df[c].mean()), "std": float(df[c].std(ddof=1)) if len(df) > 1 else 0.0}
                          for c in df.columns}
    metrics = {"model": cfg["model"], "name": cfg["name"], "approach": cfg["approach"], "best_params": best,
               "seeds": protocol["final"]["seeds"], "summary": summary, "per_seed": per_seed}
    write_json(metrics, run / "metrics.json")

    # grafy (seed 0)
    P = run / "plots"
    curves = {"validation": (yva, scores0["validation"]), "test": (yte, scores0["test"])}
    plots.roc(curves, P / "roc.png", f"{cfg['name']}: ROC krivka (seed 0)")
    plots.pr(curves, P / "pr.png", f"{cfg['name']}: precision–recall (seed 0)")
    plots.score_hist(yte, scores0["test"], res0["thresholds"], P / "score_hist_test.png", f"{cfg['name']}: rozdelenie skóre na teste")
    plots.confusion(res0["test"]["at_val_fpr"], P / "confusion_test_val_fpr.png",
                    f"Test, prah z validácie (FPR ≤ {protocol['thresholds']['target_fpr']:.0%})")
    plots.confusion(res0["test"]["at_fixed"], P / "confusion_test_fixed.png", f"Test, prah {protocol['thresholds']['fixed']}")
    plots.per_family({s: pd.DataFrame(res0[s]["at_val_fpr"]["per_family"]) for s in ("validation", "test")},
                     P / "per_family.png", f"{cfg['name']}: detekcia podľa rodiny (prah z validácie)")
    plots.learning_curve(info0, P / "learning_curve.png", f"{cfg['name']}: priebeh učenia (seed 0)")

    from src.evaluation.report import write_run_readme, update_model_index
    write_run_readme(run, cfg, protocol, metrics, timing, trials)
    update_model_index(run.parent)
    log(f"Hotovo: {rel(run)}")
    logf.close()
    return run


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--runs-root", default=None, help="iný koreň pre výsledky (napr. pri skúšobnom behu)")
    ap.add_argument("--smoke", action="store_true", help="rýchla kontrola pipeline na malej podvzorke")
    a = ap.parse_args()
    main(a.config, Path(a.runs_root) if a.runs_root else None, a.tag, a.smoke)
