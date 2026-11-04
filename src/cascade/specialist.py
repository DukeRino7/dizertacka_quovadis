r"""V3 – B (docs/12): kaskáda B so „špecialistom“ – druhým stupňom učeným iba na neistých súboroch.

1. Statický LightGBM (V1/V2) ohodnotí každý súbor; prah z validácie (FPR 1 %).
2. Eskalácia = rozpočet emulácie: súbory, ktorých skóre je najbližšie prahu (vzdialenosť v log-odds); hranica
   = kvantil `budget` vzdialenosti na validácii (rovnako ako `evaluate_b.py`).
3. Špecialista = LightGBM s hyperparametrami hybridného LightGBM (bez ladenia), učený iba na tréningových súboroch,
   ktorých OOF skóre statického LightGBM (`teachers/static_lightgbm`) leží najbližšie prahu (`train_fraction`);
   early stopping na validačných súboroch v tej istej oblasti (skóre finálneho statického modelu).
   Vstup: statické + dynamické príznaky (`features: hybrid`) alebo iba dynamické (`features: dynamic`),
   vždy + log-odds skóre statického modelu.
4. Neeskalované súbory rozhodne statický model, eskalované špecialista. Prah špecialistu sa určí na validácii tak,
   aby celá kaskáda mala FPR ≤ 1 % (pre každý rozpočet zvlášť).

Referencie na rovnakých dátach: statický, dynamický a hybridný LightGBM a kaskáda B-baselines pri rovnakom rozpočte.
Komponenty sa hľadajú v `runs_root` a v `DIZERTACKA_RESULTS_FALLBACK` (časový test: runs_final, zero-day:
runs_v2/lofo/<rodina>). Zero-day: `DIZERTACKA_HOLDOUT_FAMILY` (TPR vynechanej rodiny na teste a v januári).

    .venv\Scripts\python.exe -m src.cascade.specialist --config configs/cascade/v3_spec.yaml [--benchmark] [--smoke]
"""
import argparse
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from src.common import paths
from src.common.config import load_config
from src.common.hardware import load_protocol
from src.common.paths import PROJECT_ROOT, RUNS_DIR, rel
from src.common.provenance import environment, git_info, now_iso, write_json
from src.common.seed import set_seed
from src.data.providers import feature_names, load_tabular
from src.evaluation.metrics import at_threshold
from src.models.registry import get_model_class
from src.models.tabular import lightgbm_model
from src.training.run_tabular import class_weights
from .components import Component
from .evaluate import DEC_METRICS
from .evaluate_b import decide, logit

ROLES = {"static": "static/lightgbm", "dynamic": "dynamic/lightgbm", "hybrid": "hybrid/lightgbm"}


def result_roots(runs_root: Path) -> list[Path]:
    return [runs_root] + [PROJECT_ROOT / r for r in os.environ.get("DIZERTACKA_RESULTS_FALLBACK", "").split(";") if r]


def find_oof(runs_root: Path, teacher: str = "static_lightgbm") -> Path:
    for root in result_roots(runs_root):
        base = root / "teachers" / teacher
        runs = sorted(r for r in base.iterdir() if (r / "train_oof.parquet").exists()) if base.exists() else []
        if runs:
            return runs[-1] / "train_oof.parquet"
    raise FileNotFoundError(f"OOF skóre {teacher} nie sú v {[str(r) for r in result_roots(runs_root)]}")


def spec_threshold(y: np.ndarray, dec_s: np.ndarray, esc: np.ndarray, sp: np.ndarray, target: float) -> float:
    """Najnižší prah špecialistu, pri ktorom má celá kaskáda FPR ≤ target (neeskalované rozhoduje statický)."""
    ben = y == 0
    allowed = int(np.floor(target * ben.sum() + 1e-9)) - int((dec_s & ~esc & ben).sum())
    if allowed < 0:
        return float("inf")
    cand = np.sort(sp[esc & ben])[::-1]
    if allowed >= len(cand):
        return 0.0
    return float(np.nextafter(cand[allowed], np.inf))


def aligned_scores(comp: Component, split: str, seed: int, sha: np.ndarray) -> np.ndarray:
    d = comp.scores(split, seed).set_index("sha256")["score"]
    s = d.reindex(sha)
    if s.isna().any():
        raise ValueError(f"{comp.spec} {split}: chýbajú skóre pre {int(s.isna().sum())} súborov")
    return s.to_numpy()


def evaluate_split(y, fam_mask, s_scores: dict, thr: dict, esc, final_spec) -> dict:
    """Metriky špecialistu a referencií na jednej časti dát (s_scores: role -> skóre)."""
    D = pd.DataFrame({f"s_{r}": v for r, v in s_scores.items()})
    finals = {"spec": final_spec.astype(int),
              "b_baselines": decide(D, esc, thr, thr["static"], thr["static"], "dynamic")["final"]}
    for r in ROLES:
        finals[f"{r}_only"] = (s_scores[r] >= thr[r]).astype(int)
    out = {}
    for name, f in finals.items():
        m = at_threshold(y, f.astype(float), 0.5) if (y == 0).any() else {"recall_tpr": float(f[y == 1].mean())}
        r = {k: m[k] for k in DEC_METRICS if k in m}
        if fam_mask is not None:
            r["tpr_family"] = float(f[fam_mask].mean()) if fam_mask.any() else None
        out[name] = r
    return out


def main(config_path: str, runs_root: Path = RUNS_DIR, benchmark: bool = False, smoke: bool = False) -> Path:
    cfg = load_config(config_path)
    protocol = load_protocol(cfg.get("protocol", "configs/protocol.yaml"))
    fam = paths.HOLDOUT_FAMILY
    comps = {r: Component(spec, runs_root) for r, spec in ROLES.items()}
    oof_path = find_oof(runs_root)
    params = dict(comps["hybrid"].metrics["best_params"])   # hyperparametre hybridného LightGBM (V1), bez ladenia
    seeds = sorted(set.intersection(*(set(c.seeds) for c in comps.values())))
    if smoke:
        seeds = seeds[:1]
        params.update(num_boost_round=200, early_stopping_rounds=20)

    data = load_tabular("hybrid")
    n_static = len(feature_names("static"))
    splits = [s for s in ("validation", "test", "holdout") if s in data]
    sha = {s: data[s][2]["sha256"].to_numpy() for s in ["train"] + splits}
    oof = pd.read_parquet(oof_path).set_index("sha256")["p_teacher"].reindex(sha["train"])
    if oof.isna().any():
        raise ValueError(f"{int(oof.isna().sum())} tréningových súborov nemá OOF skóre ({rel(oof_path)})")
    oof = oof.to_numpy()

    def feats(X, s_static):
        base = X if cfg["features"] == "hybrid" else X[:, n_static:]
        return np.hstack([base, logit(s_static)[:, None]]).astype(np.float32)

    out = runs_root / "cascade" / cfg["name"] / datetime.now().strftime("%Y%m%d-%H%M%S")
    (out / "predictions").mkdir(parents=True)
    model_cls = get_model_class("lightgbm")
    budgets = sorted(set(cfg["budgets"]) | {cfg["main_budget"]})
    per_seed, model0, X0 = [], None, None
    for seed in seeds:
        thr = {r: comps[r].threshold(seed) for r in ROLES}
        lt = logit(np.array([thr["static"]]))[0]
        S = {s: {r: aligned_scores(comps[r], s, seed, sha[s]) for r in ROLES} for s in splits}
        dist = {s: np.abs(logit(S[s]["static"]) - lt) for s in splits}
        d_tr = np.abs(logit(oof) - lt)
        f = cfg["train_fraction"]
        tr = d_tr <= np.quantile(d_tr, f)
        va = dist["validation"] <= np.quantile(dist["validation"], f)
        if smoke and tr.sum() > 3000:
            keep = np.random.default_rng(0).choice(np.flatnonzero(tr), 3000, replace=False)
            tr = np.zeros_like(tr); tr[keep] = True
        Xtr, ytr = feats(data["train"][0][tr], oof[tr]), data["train"][1][tr]
        Xva_r, yva_r = feats(data["validation"][0][va], S["validation"]["static"][va]), data["validation"][1][va]
        if len(np.unique(ytr)) < 2 or len(np.unique(yva_r)) < 2:
            raise ValueError("oblasť neistoty obsahuje iba jednu triedu – špecialistu nemožno učiť")
        set_seed(seed)
        model = model_cls(params, seed=seed, threads=protocol["training_threads"])
        info = model.fit(Xtr, ytr, class_weights(ytr, protocol.get("class_weight")), Xva_r, yva_r)
        lightgbm_model._DATASET_CACHE.clear()
        model.save(out / "model" / f"seed_{seed}")
        sp = {s: model.predict_proba(feats(data[s][0], S[s]["static"])) for s in splits}
        print(f"Seed {seed}: špecialista na {int(tr.sum())} tréningových súboroch (malvér {ytr.mean():.1%}), "
              f"early stopping na {int(va.sum())} validačných, iterácie {info['best_iteration']}", flush=True)

        rec = {"seed": seed, "thresholds": thr, "train_region": {"n": int(tr.sum()), "malware_share": float(ytr.mean()),
               "cutoff_logodds": float(np.quantile(d_tr, f))}, "val_region_n": int(va.sum()),
               "best_iteration": info["best_iteration"], "budgets": {}}
        yv = data["validation"][1]
        for b in budgets:
            cut = float(np.quantile(dist["validation"], b))
            esc_v = dist["validation"] <= cut
            t_sp = spec_threshold(yv, S["validation"]["static"] >= thr["static"], esc_v, sp["validation"], protocol["thresholds"]["target_fpr"])
            rb = {"cutoff_logodds": cut, "spec_threshold": t_sp}
            for s in splits:
                y = data[s][1]
                esc = dist[s] <= cut
                final = np.where(esc, sp[s] >= t_sp, S[s]["static"] >= thr["static"])
                fm = (data[s][2]["family"].to_numpy() == fam) & (y == 1) if (fam and s == "test") else None
                rb[s] = {"emulation_rate": float(esc.mean()), "approaches": evaluate_split(y, fm, S[s], thr, esc, final)}
                if s == "test":
                    fams = data[s][2]["family"].to_numpy()
                    rb[s]["per_family_tpr"] = {g: float(final[(fams == g) & (y == 1)].mean()) for g in np.unique(fams[y == 1])}
            rec["budgets"][str(b)] = rb
        main_cut = rec["budgets"][str(cfg["main_budget"])]["cutoff_logodds"]
        for s in splits:
            data[s][2][["sha256", "family", "label"]].assign(
                score=sp[s], s_static=S[s]["static"], escalated_main=dist[s] <= main_cut
            ).to_parquet(out / "predictions" / f"{s}_seed{seed}.parquet", index=False)
        per_seed.append(rec)
        if model0 is None:
            model0, X0 = model, feats(data["test"][0], S["test"]["static"])

    summary = summarize(per_seed, splits)
    bench = run_benchmark(model0, X0, protocol, smoke) if benchmark else None
    costs = None
    if bench and comps["static"].cost():
        emu = summary[str(cfg["main_budget"])]["test"]["emulation_rate"][0]
        c_s = comps["static"].cost()
        costs = {"static_cpu_ms_batch": c_s["cpu_ms_batch"], "spec_cpu_ms_batch": bench["cpu_batch"]["cpu_ms_per_sample"],
                 "cascade_cpu_ms_batch": c_s["cpu_ms_batch"] + emu * bench["cpu_batch"]["cpu_ms_per_sample"],
                 "emulation_rate": emu}
    write_json({"created": now_iso(), "type": "V3-specialist", "config": cfg, "git": git_info(), "holdout_family": fam,
                "components": {r: rel(c.run) for r, c in comps.items()}, "oof": rel(oof_path), "params": params,
                "seeds": seeds, "smoke": smoke, "summary": summary, "per_seed": per_seed, "costs": costs}, out / "metrics.json")
    if bench:
        write_json({**bench, "environment": environment()}, out / "benchmark.json")
    write_readme(out, cfg, comps, oof_path, seeds, summary, costs, fam)
    print(f"Špecialista vyhodnotený: {rel(out)}")
    return out


def summarize(per_seed: list, splits: list) -> dict:
    def ms(v):
        v = [x for x in v if x is not None]
        return [float(np.mean(v)), float(np.std(v, ddof=1)) if len(v) > 1 else 0.0] if v else None
    S = {}
    for b in per_seed[0]["budgets"]:
        S[b] = {}
        for s in splits:
            rows = [p["budgets"][b][s] for p in per_seed]
            S[b][s] = {"emulation_rate": ms([r["emulation_rate"] for r in rows]),
                       "approaches": {a: {k: ms([r["approaches"][a].get(k) for r in rows]) for k in rows[0]["approaches"][a]}
                                      for a in rows[0]["approaches"]}}
            if s == "test":
                S[b][s]["per_family_tpr"] = {g: ms([r["per_family_tpr"][g] for r in rows]) for g in rows[0]["per_family_tpr"]}
    return S


def run_benchmark(model, X, protocol: dict, smoke: bool) -> dict:
    from src.evaluation.benchmark import _batch, _single
    cfg = dict(protocol["benchmark"])
    if smoke:
        cfg.update(min_seconds=1, single_samples=50)
    X = np.ascontiguousarray(X)
    out = {"created": now_iso(), "n_test": int(len(X)), "config": cfg}
    model.set_threads(cfg["batch_threads"])
    with threadpool_limits(cfg["batch_threads"]):
        out["cpu_batch"] = _batch(model.predict_proba, X, cfg["min_seconds"], False, None)
    model.set_threads(1)
    with threadpool_limits(1):
        out["cpu_single"] = _single(model.predict_proba, X, cfg["single_samples"], cfg["warmup"], False, None, cfg["min_seconds"])
    print(f"Meranie špecialistu: {out['cpu_batch']['cpu_ms_per_sample']:.4f} ms CPU/vz. (dávka)", flush=True)
    return out


LABELS = {"spec": "kaskáda so špecialistom", "b_baselines": "kaskáda B-baselines (rovnaký rozpočet)",
          "static_only": "statický LightGBM", "dynamic_only": "dynamický LightGBM", "hybrid_only": "hybrid LightGBM"}


def write_readme(out, cfg, comps, oof_path, seeds, S, costs, fam):
    def f(v):
        return "–" if v is None else f"{v[0]:.4f} ± {v[1]:.4f}"
    mb = str(cfg["main_budget"])
    t = S[mb]["test"]
    cols = ["recall_tpr", "fpr", "f1"] + (["tpr_family"] if fam else [])
    head = "| prístup | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols)
    rows = "\n".join(f"| {LABELS[a]} | " + " | ".join(f(t["approaches"][a].get(c)) for c in cols) + " |" for a in LABELS)
    hold = ""
    if "holdout" in S[mb]:
        h = S[mb]["holdout"]["approaches"]
        hold = "\n## Januárové vzorky vynechanej rodiny (TPR)\n| prístup | TPR |\n|---|---|\n" + \
               "\n".join(f"| {LABELS[a]} | {f(h[a]['recall_tpr'])} |" for a in LABELS) + "\n"
    curve = "| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |" + \
            ("TPR vynech. rodiny špecialista |" if fam else "") + "\n|---|---|---|---|---|---|" + ("---|" if fam else "") + "\n" + \
            "\n".join(f"| {b} | {S[b]['test']['emulation_rate'][0]:.4f} | {S[b]['test']['approaches']['spec']['recall_tpr'][0]:.4f} | "
                      f"{S[b]['test']['approaches']['spec']['fpr'][0]:.4f} | {S[b]['test']['approaches']['b_baselines']['recall_tpr'][0]:.4f} | "
                      f"{S[b]['test']['approaches']['b_baselines']['fpr'][0]:.4f} |"
                      + (f" {S[b]['test']['approaches']['spec']['tpr_family'][0]:.4f} |" if fam else "") for b in S)
    cost = (f"CPU ms/vz. (dávka): statický {costs['static_cpu_ms_batch']:.4f} + {costs['emulation_rate']:.1%} × špecialista "
            f"{costs['spec_cpu_ms_batch']:.4f} = **{costs['cascade_cpu_ms_batch']:.4f}** (odhad zo súčtu komponentov).") if costs else \
        "_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._"
    text = f"""# V3 – špecialista `{cfg['name']}` – beh `{out.name}`

> Generované `src/cascade/specialist.py` ({now_iso()}). Plán: `docs/12_plan_v3.md`. Seedy {seeds}, priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
{f'> Zero-day: vynechaná rodina **{fam}**.' if fam else '> Časový test (rozdelenie V1).'}

Vstup špecialistu: **{cfg['features']}** + log-odds statického skóre; tréning na {cfg['train_fraction']:.0%} tréningu najbližšie
prahu (OOF skóre `{rel(oof_path)}`). Komponenty: {', '.join(f'{r} `{rel(c.run)}`' for r, c in comps.items())}.

## Test – hlavný rozpočet {float(mb):.0%} (emulované {t['emulation_rate'][0]:.2%} súborov)
{head}
{rows}
{hold}
## Krivka rozpočtu (test, priemer cez seedy)
{curve}

## Výpočtové nároky
{cost}
"""
    (out / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--runs-root", default=None)
    ap.add_argument("--benchmark", action="store_true", help="zmerať CPU čas špecialistu (iba časový test)")
    ap.add_argument("--smoke", action="store_true", help="technická kontrola: 1 seed, ≤ 3000 tréningových súborov")
    a = ap.parse_args()
    main(a.config, Path(a.runs_root) if a.runs_root else RUNS_DIR, a.benchmark, a.smoke)
