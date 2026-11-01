"""Analýza, ktoré príznaky modely využívajú (hľadanie skratiek a artefaktov datasetu).

Počíta sa IBA na validácii (test sa nepoužíva), z modelu seedu 0 posledného behu.
Metódy:
1. Permutačná dôležitosť skupín (pre všetky modely): náhodné premiešanie celej skupiny príznakov
   (riadky bloku sa premiešajú spolu) -> pokles ROC-AUC. Veľký pokles = model sa na skupinu spolieha.
2. Permutačná dôležitosť sledovaných príznakov (configs/analysis/feature_importance.yaml).
3. Vlastná dôležitosť modelu, ak existuje: LightGBM – priemerná |SHAP| hodnota (TreeSHAP, pred_contrib)
   a gain; LR – |koeficient| na štandardizovaných vstupoch; RF – pokles nečistoty (skreslené k príznakom
   s mnohými hodnotami, iba orientačne). MLP nemá vlastnú mieru -> iba permutácia.

Spustenie:
    .venv\\Scripts\\python.exe -m src.evaluation.feature_importance --approach static
"""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.common.config import load_config
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import now_iso, write_json
from src.data.providers import load_tabular
from src.models.registry import get_model_class
from . import plots as P
from .compare import ORDER, latest_runs


def load_pipeline(run: Path):
    cfg = load_config(run / "config.yaml")
    model = get_model_class(cfg["model"]).load(run / "model" / "seed_0")
    model.set_threads(-1)
    pre_path = run / "model" / "preprocessor.joblib"
    pre = joblib.load(pre_path) if pre_path.exists() else None
    mask_path = run / "model" / "feature_mask.json"
    cols = np.array(json.loads(mask_path.read_text())["kept_columns"]) if mask_path.exists() else None
    return cfg, model, pre, cols


def permutation_drop(score_fn, X, y, blocks: dict[str, np.ndarray], repeats: int, seed: int) -> pd.DataFrame:
    base = roc_auc_score(y, score_fn(X))
    rng = np.random.default_rng(seed)
    rows = []
    for name, cols in blocks.items():
        drops = []
        for _ in range(repeats):
            Xp = X.copy()
            Xp[:, cols] = X[rng.permutation(len(X))][:, cols]
            drops.append(base - roc_auc_score(y, score_fn(Xp)))
        rows.append({"name": name, "n_features": len(cols), "auc_drop_mean": float(np.mean(drops)),
                     "auc_drop_std": float(np.std(drops, ddof=1)) if repeats > 1 else 0.0})
    return pd.DataFrame(rows).assign(base_auc=base).sort_values("auc_drop_mean", ascending=False)


def native_importance(cfg, model, pre, Xin: np.ndarray, names: list[str], shap_rows: int, seed: int) -> pd.DataFrame | None:
    """Vlastná dôležitosť modelu na pôvodných menách príznakov (Xin = vstup modelu pred transformáciou)."""
    kind = cfg["model"]
    if kind == "lightgbm":
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(Xin), min(shap_rows, len(Xin)), replace=False)
        contrib = model.model.predict(Xin[idx], pred_contrib=True)[:, :-1]  # posledný stĺpec = bias
        return pd.DataFrame({"name": names, "mean_abs_shap": np.abs(contrib).mean(axis=0),
                             "gain": model.model.feature_importance("gain")}).sort_values("mean_abs_shap", ascending=False)
    if kind == "logreg":
        coef = np.zeros(len(names))
        coef[np.flatnonzero(pre.keep_)] = model.model.coef_[0]
        return pd.DataFrame({"name": names, "abs_coef": np.abs(coef), "coef": coef}).sort_values("abs_coef", ascending=False)
    if kind == "random_forest":
        return pd.DataFrame({"name": names, "impurity_importance": model.model.feature_importances_}) \
            .sort_values("impurity_importance", ascending=False)
    return None


def analyze_run(run: Path, approach: str, data, feats: pd.DataFrame, acfg: dict) -> dict:
    cfg, model, pre, cols = load_pipeline(run)
    X, y, _ = data
    if acfg.get("validation_rows") and len(y) > acfg["validation_rows"]:
        idx = np.sort(np.random.default_rng(acfg["seed"]).choice(len(y), acfg["validation_rows"], replace=False))
        X, y = X[idx], y[idx]
    f = feats if cols is None else feats.iloc[cols].reset_index(drop=True)
    Xin = X if cols is None else X[:, cols]
    names = f["name"].tolist()

    def score(Z):
        return model.predict_proba(pre.transform(Z) if pre is not None else Z)

    groups = {g: np.flatnonzero(f["group"].to_numpy() == g) for g in f["group"].unique()}
    watch = {n: np.array([names.index(n)]) for n in acfg["watch_features"] if n in names}
    out_dir = run / "importance"
    (out_dir).mkdir(exist_ok=True)
    g_df = permutation_drop(score, Xin, y, groups, acfg["repeats"], acfg["seed"])
    w_df = permutation_drop(score, Xin, y, watch, acfg["repeats"], acfg["seed"]) if watch else pd.DataFrame()
    n_df = native_importance(cfg, model, pre, Xin, names, acfg["shap_rows"], acfg["seed"])
    g_df.to_csv(out_dir / "group_permutation.csv", index=False)
    if not w_df.empty:
        w_df.to_csv(out_dir / "watch_permutation.csv", index=False)
    if n_df is not None:
        n_df = n_df.merge(f[["name", "group"]], on="name")
        n_df.to_csv(out_dir / "native_importance.csv", index=False)

    # grafy
    plot_drop(g_df, out_dir / "group_permutation.png", f"{cfg['name']}: pokles ROC-AUC po premiešaní skupiny")
    if not w_df.empty:
        plot_drop(w_df, out_dir / "watch_permutation.png", f"{cfg['name']}: pokles ROC-AUC po premiešaní príznaku")
    if n_df is not None:
        col = n_df.columns[1]
        plot_top(n_df.head(acfg["top_k"]), col, out_dir / "top_native.png",
                 f"{cfg['name']}: top {acfg['top_k']} príznakov")

    res = {"created": now_iso(), "run": rel(run), "model": cfg["name"], "validation_rows": int(len(y)),
           "base_auc": float(g_df["base_auc"].iloc[0]), "groups": g_df.drop(columns="base_auc").to_dict("records"),
           "watch": w_df.drop(columns="base_auc").to_dict("records") if not w_df.empty else [],
           "native_top": n_df.head(acfg["top_k"]).to_dict("records") if n_df is not None else None}
    write_json(res, out_dir / "importance.json")
    return res


def plot_drop(df: pd.DataFrame, path: Path, title: str):
    fig, ax = P._fig(7.5, 0.45 * len(df) + 1.6)
    y = np.arange(len(df))[::-1]
    ax.barh(y, df["auc_drop_mean"], xerr=df["auc_drop_std"], height=0.6, color=P.SPLIT_COLOR["validation"],
            error_kw={"ecolor": P.INK, "capsize": 3, "linewidth": 1})
    for yi, v, e in zip(y, df["auc_drop_mean"], df["auc_drop_std"]):
        ax.text(max(v, 0) + e, yi, f"  {v:.4f}", va="center", color=P.INK, fontsize=9)
    ax.set_yticks(y, df["name"])
    ax.set_xlim(min(0, df["auc_drop_mean"].min() * 1.2), max((df["auc_drop_mean"] + df["auc_drop_std"]).max() * 1.35, 1e-4))
    P._style(ax, title, "pokles ROC-AUC na validácii (väčší = dôležitejšie)", "", grid="x")
    P._save(fig, path)


def plot_top(df: pd.DataFrame, col: str, path: Path, title: str):
    fig, ax = P._fig(8, 0.32 * len(df) + 1.6)
    y = np.arange(len(df))[::-1]
    ax.barh(y, df[col], height=0.65, color=P.SPLIT_COLOR["train"])
    ax.set_yticks(y, [f"{n}  ({g})" for n, g in zip(df["name"], df["group"])], fontsize=8)
    labels = {"mean_abs_shap": "priemerná |SHAP| hodnota (validácia)", "abs_coef": "|koeficient| (štandardizované vstupy)",
              "impurity_importance": "pokles nečistoty (orientačné)"}
    P._style(ax, "", labels.get(col, col), "", grid="x")
    fig.suptitle(title, x=0.02, ha="left", color=P.INK, fontsize=12)
    P._save(fig, path)


def write_summary(results: list[dict], approach: str, watch: list[str]):
    out = RUNS_DIR / "comparison" / approach
    out.mkdir(parents=True, exist_ok=True)
    res = sorted(results, key=lambda r: ORDER.index(r["model"]) if r["model"] in ORDER else 99)
    groups = [g["name"] for g in res[0]["groups"]]
    lines = ["| skupina | " + " | ".join(r["model"] for r in res) + " |", "|---|" + "---|" * len(res)]
    for g in groups:
        vals = [next((x["auc_drop_mean"] for x in r["groups"] if x["name"] == g), np.nan) for r in res]
        lines.append(f"| {g} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")
    wl = ["| príznak | " + " | ".join(r["model"] for r in res) + " |", "|---|" + "---|" * len(res)]
    for n in watch:
        vals = [next((x["auc_drop_mean"] for x in r["watch"] if x["name"] == n), np.nan) for r in res]
        wl.append(f"| `{n}` | " + " | ".join("–" if np.isnan(v) else f"{v:.4f}" for v in vals) + " |")
    text = f"""# Využívanie príznakov – {approach}

> Generované `src/evaluation/feature_importance.py` ({now_iso()}). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
{chr(10).join(lines)}

## Sledované príznaky (možné artefakty datasetu)
{chr(10).join(wl)}

Interpretácia: pokles blízko 0 = model sa bez príznaku zaobíde (často preto, že rovnakú informáciu nesú iné príznaky).
Permutácia jedného príznaku podhodnocuje skupinu korelovaných príznakov – preto aj kontrolný experiment bez nich
(`runs/comparison/static_ablations/`).
"""
    (out / "IMPORTANCE.md").write_text(text, encoding="utf-8")
    print(f"Súhrn: {rel(out / 'IMPORTANCE.md')}")


def main(approach: str, models: list[str] | None):
    acfg = load_config("configs/analysis/feature_importance.yaml")
    from src.data.providers import feature_table
    feats = feature_table(approach)
    data = load_tabular(approach, splits=("validation",))["validation"]
    results = []
    for name, run in latest_runs(approach).items():
        if models and name not in models:
            continue
        if load_config(run / "config.yaml")["approach"] != approach:   # napr. sekvenčné modely – nemajú tabuľkové príznaky
            print(f"{approach}/{name}: preskočené (iný typ vstupu)", flush=True)
            continue
        print(f"{approach}/{name}: analýza príznakov ...", flush=True)
        results.append(analyze_run(run, approach, data, feats, acfg))
    if results:
        write_summary(results, approach, acfg["watch_features"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="static")
    ap.add_argument("--models", nargs="*", default=None)
    a = ap.parse_args()
    main(a.approach, a.models)
