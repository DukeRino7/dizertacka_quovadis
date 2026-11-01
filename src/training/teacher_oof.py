"""Mäkké označenia učiteľa na tréningu krížovo (out-of-fold) pre destiláciu vedomostí.

Učiteľ je na vlastných tréningových dátach príliš istý (napr. RF má na tréningu ROC-AUC 1,0) – jeho predikcie
by nenesli „tmavé vedomosti“. Preto sa tréning rozdelí na K častí (stratifikovane podľa rodiny, skupiny identických
EMBER vektorov spolu) a každú časť predpovedá učiteľ natrénovaný na zvyšných K−1 častiach s rovnakými
hyperparametrami ako finálny učiteľ (z jeho behu). Validácia slúži iba na early stopping (ako pri finálnom učiteľovi).

    .venv\\Scripts\\python.exe -m src.training.teacher_oof --teacher hybrid/two_branch
Výstup: runs/teachers/<prístup>_<model>/<dátum-čas>/train_oof.parquet (sha256, label, family, fold, p_teacher),
        manifest.json, README.md
"""
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

from src.cascade.components import resolve_run
from src.common.config import load_config
from src.common.hardware import load_protocol
from src.common.paths import INDEX_DIR, RUNS_DIR, rel
from src.common.provenance import git_info, now_iso, write_json
from src.common.seed import set_seed
from src.data.providers import load_tabular
from src.data.static_transforms import StaticPreprocessor
from src.models.registry import get_model_class
from .run_tabular import class_weights


def main(teacher: str, folds: int, seed: int, runs_root: Path = RUNS_DIR, limit: int | None = None) -> Path:
    t0 = time.perf_counter()
    run = resolve_run(teacher, runs_root)
    cfg = load_config(run / "config.yaml")
    protocol = load_protocol()  # vlákna podľa aktuálneho počítača; ostatné pravidlá sú rovnaké
    best = json.loads((run / "metrics.json").read_text(encoding="utf-8"))["best_params"]
    model_cls = get_model_class(cfg["model"])

    data = load_tabular(cfg["approach"], splits=("train", "validation"))
    Xtr, ytr, mtr = data["train"]; Xva, yva, _ = data["validation"]
    mask = run / "model" / "feature_mask.json"
    if mask.exists():
        cols = np.array(json.loads(mask.read_text())["kept_columns"])
        Xtr, Xva = Xtr[:, cols], Xva[:, cols]
    if limit:  # iba technická kontrola
        Xtr, ytr, mtr = Xtr[:limit], ytr[:limit], mtr.iloc[:limit].reset_index(drop=True)
    groups = mtr[["sha256"]].merge(pd.read_parquet(INDEX_DIR / "samples.parquet", columns=["sha256", "feature_group"]),
                                   on="sha256", how="left")["feature_group"].to_numpy()

    oof = np.full(len(ytr), np.nan)
    fold_id = np.full(len(ytr), -1)
    fold_info = []
    sgkf = StratifiedGroupKFold(n_splits=folds, shuffle=True, random_state=seed)
    for k, (tr_idx, ho_idx) in enumerate(sgkf.split(np.zeros(len(ytr)), mtr["family"], groups)):
        set_seed(seed)
        Xa, Xh, Xv = Xtr[tr_idx], Xtr[ho_idx], Xva
        if model_cls.needs_scaling:  # rovnaké predspracovanie ako v run_tabular, fit iba na trénovacej časti foldu
            pre = StaticPreprocessor().fit(Xa)
            Xa, Xh, Xv = pre.transform(Xa), pre.transform(Xh), pre.transform(Xv)
        m = model_cls(best, seed=seed, threads=protocol["training_threads"])
        t = time.perf_counter()
        m.fit(Xa, ytr[tr_idx], class_weights(ytr[tr_idx], protocol.get("class_weight")), Xv, yva)
        oof[ho_idx] = m.predict_proba(Xh)
        fold_id[ho_idx] = k
        auc = roc_auc_score(ytr[ho_idx], oof[ho_idx])
        fold_info.append({"fold": k, "n_train": len(tr_idx), "n_holdout": len(ho_idx), "holdout_auc": auc,
                          "fit_s": time.perf_counter() - t})
        print(f"  fold {k}: AUC na odloženej časti {auc:.5f} ({fold_info[-1]['fit_s']:.0f} s)", flush=True)
    assert not np.isnan(oof).any()

    out = runs_root / "teachers" / f"{cfg.get('results_approach', cfg['approach'])}_{cfg['name']}" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    df = mtr[["sha256", "family", "label"]].assign(fold=fold_id, p_teacher=oof)
    df.to_parquet(out / "train_oof.parquet", index=False)
    total_auc = roc_auc_score(ytr, oof)
    write_json({"created": now_iso(), "teacher_run": rel(run), "teacher_model": cfg["model"], "data_approach": cfg["approach"],
                "folds": folds, "seed": seed, "best_params": best, "oof_auc": total_auc, "fold_info": fold_info,
                "limit": limit, "duration_s": time.perf_counter() - t0, "git": git_info()}, out / "manifest.json")
    (out / "README.md").write_text(f"""# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` ({now_iso()}).

- Učiteľ: `{rel(run)}` (`{cfg['model']}`, vstup `{cfg['approach']}`), hyperparametre z jeho behu.
- {folds} častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed {seed}).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **{total_auc:.5f}**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): {float(((oof < 0.01) | (oof > 0.99)).mean()):.3f}
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie {time.perf_counter() - t0:.0f} s.
""", encoding="utf-8")
    print(f"Mäkké označenia: {rel(out)} (OOF AUC {total_auc:.5f})")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--teacher", required=True, help="'<prístup>/<model>' (posledný beh) alebo cesta k behu učiteľa")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--runs-root", default=None)
    ap.add_argument("--limit", type=int, default=None, help="iba technická kontrola na prvých N vzorkách")
    a = ap.parse_args()
    main(a.teacher, a.folds, a.seed, Path(a.runs_root) if a.runs_root else RUNS_DIR, a.limit)
