"""Kaskáda B (docs/09): najprv statický model; iba pri neistom skóre emulácia a druhý stupeň.

1. Statický model ohodnotí každý súbor. Skóre ≥ `hi` → malvér, skóre < `lo` → neškodný (bez emulácie).
   `hi` = prah s FPR ≤ `fpr_hi` na validácii, `lo` = pod ním leží najviac `fnr_lo` malvéru validácie.
2. Neisté súbory (lo ≤ skóre < hi) sa emulujú:
   - `second_stage: dynamic` – dynamický model; ak sa zhodne so statickým (oba pri prahoch z validácie, FPR ≤ 1 %),
     rozhodnutie platí, inak rozhodne hybridný model,
   - `second_stage: hybrid` – rovno hybridný model.
3. Doplnková krivka: pevné rozpočty emulácie – emulujú sa súbory najbližšie prahu statického modelu (vzdialenosť
   v log-odds); hranica vzdialenosti sa určí na validácii a použije na teste.

Všetko z uložených predikcií; prahy iba z validácie. Ak komponenty majú predikcie `holdout` (januárové vzorky
vynechanej rodiny pri zero-day behu), vyhodnotí sa na nich TPR.

    .venv\\Scripts\\python.exe -m src.cascade.evaluate_b --config configs/cascade/b_main.yaml
"""
import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.config import load_config
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import git_info, now_iso, write_json
from src.evaluation import plots as P
from src.evaluation.metrics import at_threshold, threshold_for_fpr
from .components import Component
from .evaluate import DEC_METRICS, _merge

EPS = 1e-6


def logit(p):
    p = np.clip(p, EPS, 1 - EPS)
    return np.log(p / (1 - p))


def band(sv: np.ndarray, yv: np.ndarray, fpr_hi: float, fnr_lo: float) -> tuple[float, float]:
    """Pásmo neistoty statického modelu z validácie: (lo, hi)."""
    hi = threshold_for_fpr(yv, sv, fpr_hi)
    lo = float(np.quantile(sv[yv == 1], fnr_lo, method="lower"))   # skóre < lo má najviac fnr_lo malvéru
    return min(lo, hi), hi


def decide(D: pd.DataFrame, uncertain: np.ndarray, thr: dict, lo: float, hi: float, second: str) -> dict:
    """Rozhodnutia kaskády B na jednej časti dát."""
    s = D["s_static"].to_numpy()
    dec_s = (s >= thr["static"]).astype(int)
    dec_h = (D["s_hybrid"].to_numpy() >= thr["hybrid"]).astype(int)
    final = np.where(s >= hi, 1, 0)                     # isté rozhodnutie statického modelu (mimo pásma)
    if second == "dynamic":
        dec_d = (D["s_dynamic"].to_numpy() >= thr["dynamic"]).astype(int)
        to_hybrid = uncertain & (dec_d != dec_s)
        final = np.where(uncertain, np.where(to_hybrid, dec_h, dec_s), final)
    else:
        to_hybrid = uncertain
        final = np.where(uncertain, dec_h, final)
    return {"final": final, "emulated": uncertain, "to_hybrid": to_hybrid}


def evaluate_seed(comps: dict, cfg: dict, seed: int) -> dict:
    second = cfg["second_stage"]
    roles = list(comps)
    V = _merge(comps, "validation", seed)
    thr = {r: comps[r].threshold(seed) for r in roles}
    yv, sv = V["label"].to_numpy(), V["s_static"].to_numpy()
    u = cfg["uncertainty"]
    lo, hi = band(sv, yv, u["fpr_hi"], u["fnr_lo"])
    # rozpočty emulácie: hranica vzdialenosti od prahu statického modelu z validácie
    dist_v = np.abs(logit(sv) - logit(thr["static"]))
    budgets = {b: float(np.quantile(dist_v, b)) for b in cfg.get("budgets", [])}

    out = {"seed": seed, "thresholds": thr, "band": {"lo": lo, "hi": hi}, "budget_cutoffs": budgets}
    splits = ["validation", "test"] + (["holdout"] if all(c.has_split("holdout", seed) for c in comps.values()) else [])
    for split in splits:
        D = V if split == "validation" else _merge(comps, split, seed)
        y, s = D["label"].to_numpy(), D["s_static"].to_numpy()
        res = {"n": len(D)}
        main = decide(D, (s >= lo) & (s < hi), thr, lo, hi, second)
        res["approaches"] = {"cascade_b": at_threshold(y, main["final"].astype(float), 0.5)}
        for r in roles:
            res["approaches"][f"{r}_only"] = at_threshold(y, D[f"s_{r}"].to_numpy(), thr[r])
        res["cascade"] = {
            "emulation_rate": float(main["emulated"].mean()), "n_emulated": int(main["emulated"].sum()),
            "hybrid_rate": float(main["to_hybrid"].mean()), "n_hybrid": int(main["to_hybrid"].sum()),
            "confident_errors": int(((~main["emulated"]) & (main["final"] != y)).sum()),
            "per_family": (pd.DataFrame({"family": D["family"], "emu": main["emulated"], "hyb": main["to_hybrid"],
                                         "wrong": main["final"] != y})
                           .groupby("family").agg(n=("emu", "size"), emulation_rate=("emu", "mean"),
                                                  hybrid_rate=("hyb", "mean"), error_rate=("wrong", "mean"))
                           .reset_index().to_dict("records")),
        }
        dist = np.abs(logit(s) - logit(thr["static"]))
        curve = []
        for b, c in budgets.items():
            # rozpočet: neisté = najbližšie prahu; mimo pásma rozhodne statický model pri svojom prahu
            d = decide(D, dist <= c, thr, thr["static"], thr["static"], second)
            m = at_threshold(y, d["final"].astype(float), 0.5)
            curve.append({"budget_val": b, "emulation_rate": float(d["emulated"].mean()),
                          "hybrid_rate": float(d["to_hybrid"].mean()), **{k: m[k] for k in DEC_METRICS}})
        res["budget_curve"] = curve
        out[split] = res
    return out


def mean_std(vals):
    return float(np.mean(vals)), (float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0)


def summarize(per_seed: list) -> dict:
    S = {}
    for split in ("validation", "test", "holdout"):
        if split not in per_seed[0]:
            continue
        names = per_seed[0][split]["approaches"].keys()
        S[split] = {a: {m: mean_std([p[split]["approaches"][a][m] for p in per_seed]) for m in DEC_METRICS} for a in names}
        for k in ("emulation_rate", "hybrid_rate"):
            S[split][f"_{k}"] = mean_std([p[split]["cascade"][k] for p in per_seed])
        curve = pd.DataFrame([dict(r, seed=p["seed"]) for p in per_seed for r in p[split]["budget_curve"]])
        S[split]["_budget_curve"] = (curve.drop(columns="seed").groupby("budget_val").mean().reset_index().to_dict("records")
                                     if len(curve) else [])
    return S


def cost_table(comps: dict, emu: float, hyb: float, second: str, emu_s: float) -> pd.DataFrame | None:
    c = {r: comps[r].cost() for r in comps}
    if any(v is None for v in c.values()):
        return None
    rows = []
    for key, label in [("cpu_ms_batch", "CPU čas ms/vz. (dávka)"), ("cpu_ms_single", "CPU čas ms/vz. (1 vz.)")]:
        s, h = c["static"][key], c["hybrid"][key]
        d = c["dynamic"][key] if "dynamic" in c else 0.0
        casc = s + (emu * d + hyb * h if second == "dynamic" else emu * h)
        row = {"meranie": label, "statický": s}
        if "dynamic" in c:
            row["dynamický"] = d
        rows.append({**row, "hybrid na každej vzorke": h, "kaskáda B (odhad)": casc})
    return pd.DataFrame(rows)


def main(config_path: str, runs_root: Path = RUNS_DIR) -> Path:
    cfg = load_config(config_path)
    roles = ["static", "dynamic", "hybrid"] if cfg["second_stage"] == "dynamic" else ["static", "hybrid"]
    comps = {r: Component(cfg["components"][r], runs_root) for r in roles}
    seeds = sorted(set.intersection(*(set(c.seeds) for c in comps.values())))
    per_seed = [evaluate_seed(comps, cfg, s) for s in seeds]
    S = summarize(per_seed)
    emu_s = float(cfg.get("assumed_emulation_s", 60))
    costs = cost_table(comps, S["test"]["_emulation_rate"][0], S["test"]["_hybrid_rate"][0], cfg["second_stage"], emu_s)

    out = runs_root / "cascade" / cfg["name"] / datetime.now().strftime("%Y%m%d-%H%M%S")
    (out / "plots").mkdir(parents=True)
    write_json({"created": now_iso(), "type": "B", "config": cfg, "git": git_info(),
                "components": {r: rel(c.run) for r, c in comps.items()}, "seeds": seeds, "summary": S,
                "per_seed": per_seed, "costs": costs.to_dict("records") if costs is not None else None,
                "assumed_emulation_s": emu_s}, out / "metrics.json")
    plot_curve(S["test"]["_budget_curve"], S["test"], out / "plots" / "budget_curve_test.png")
    plot_family(per_seed[0]["test"]["cascade"]["per_family"], out / "plots" / "emulation_by_family.png")
    write_readme(out, cfg, comps, seeds, S, per_seed, costs, emu_s)
    print(f"Kaskáda B vyhodnotená: {rel(out)}")
    return out


LABELS = {"cascade_b": "kaskáda B", "static_only": "statický", "dynamic_only": "dynamický", "hybrid_only": "hybrid (každá vzorka)"}


def plot_curve(curve, S, path):
    """Dva panely: TPR a FPR podľa podielu emulovaných súborov (rozdielne škály, preto nie jedna os)."""
    if not curve:
        return
    d = pd.DataFrame(curve)
    x = d["emulation_rate"] * 100
    fig, axes = P.plt.subplots(1, 2, figsize=(10, 4.2), facecolor=P.SURFACE)
    for ax, m, lab, col in [(axes[0], "recall_tpr", "TPR (zachytený malvér)", P.SPLIT_COLOR["train"]),
                            (axes[1], "fpr", "FPR (falošné poplachy)", P.SPLIT_COLOR["test"])]:
        ax.set_facecolor(P.SURFACE)
        ax.plot(x, d[m], marker="o", color=col, label="rozpočty emulácie")
        ax.scatter([S["_emulation_rate"][0] * 100], [S["cascade_b"][m][0]], s=140, marker="*",
                   color=P.SPLIT_COLOR["validation"], zorder=4, label="pásmo neistoty (hlavný bod)")
        ax.axhline(S["static_only"][m][0], color=P.INK2, linestyle="--", linewidth=1, label="iba statický model")
        P._style(ax, lab, "emulované súbory [%]", "", grid="both")
    axes[0].legend(frameon=False, labelcolor=P.INK2, loc="best", fontsize=8)
    fig.suptitle("Kaskáda B na teste: kvalita vs. podiel emulovaných súborov", x=0.01, ha="left", color=P.INK)
    P._save(fig, path)


def plot_family(rows, path):
    d = pd.DataFrame(rows)
    fams = ["benign"] + sorted(f for f in d["family"] if f != "benign")
    d = d.set_index("family").reindex([f for f in fams if f in set(d.index)])
    fig, ax = P._fig(7.5, 4.6)
    y = np.arange(len(d))[::-1]
    ax.barh(y, d["emulation_rate"] * 100, height=0.6, color=P.SPLIT_COLOR["validation"])
    for yi, v in zip(y, d["emulation_rate"] * 100):
        ax.text(v, yi, f"  {v:.1f} %", va="center", color=P.INK, fontsize=9)
    ax.set_yticks(y, list(d.index))
    P._style(ax, "Kaskáda B: podiel emulovaných súborov podľa rodiny (test, seed 0)", "emulované súbory [%]", "", grid="x")
    P._save(fig, path)


def _tbl(df: pd.DataFrame, fmt="{:.4f}") -> str:
    cols = list(df.columns)
    return "\n".join(["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)] +
                     ["| " + " | ".join(fmt.format(v) if isinstance(v, float) else str(v) for v in r) + " |"
                      for r in df.itertuples(index=False)])


def write_readme(out, cfg, comps, seeds, S, per_seed, costs, emu_s):
    def block(split):
        rows = [{"prístup": LABELS[a], **{m: f"{S[split][a][m][0]:.4f} ± {S[split][a][m][1]:.4f}" for m in DEC_METRICS}}
                for a in LABELS if a in S[split]]
        return _tbl(pd.DataFrame(rows))
    t = S["test"]
    emu, hyb = t["_emulation_rate"][0], t["_hybrid_rate"][0]
    c0 = per_seed[0]["test"]["cascade"]
    curve = pd.DataFrame(t["_budget_curve"])[["budget_val", "emulation_rate", "hybrid_rate", "recall_tpr", "fpr", "f1"]] \
        if t["_budget_curve"] else None
    band_txt = ", ".join(f"seed {p['seed']}: lo = {p['band']['lo']:.4f}, hi = {p['band']['hi']:.4f}" for p in per_seed)
    holdout = ""
    if "holdout" in S:
        h = S["holdout"]
        holdout = "\n## Januárové vzorky vynechanej rodiny (iba malvér → TPR)\n" + _tbl(pd.DataFrame(
            [{"prístup": LABELS[a], "TPR": f"{h[a]['recall_tpr'][0]:.4f} ± {h[a]['recall_tpr'][1]:.4f}"} for a in LABELS if a in h])) + \
            f"\n\nPodiel emulovaných: {h['_emulation_rate'][0]:.2%}\n"
    cost_txt = _tbl(costs) if costs is not None else "_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._"
    text = f"""# Kaskáda B `{cfg['name']}` – beh `{out.name}`

> Generované `src/cascade/evaluate_b.py` ({now_iso()}). Seedy: {seeds}; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
""" + "\n".join(f"| {r} | `{rel(c.run)}` |" for r, c in comps.items()) + f"""

Druhý stupeň: **{cfg['second_stage']}**. Pásmo neistoty statického modelu: FPR ≤ {cfg['uncertainty']['fpr_hi']:.1%} nad `hi`,
najviac {cfg['uncertainty']['fnr_lo']:.0%} malvéru validácie pod `lo` ({band_txt}).

## Test
{block('test')}

- **emulované súbory: {emu:.2%}** (ostatné rozhodne iba statický model); na hybrid ide {hyb:.2%} súborov
- chyby pri istom rozhodnutí statického modelu (seed {seeds[0]}): {c0['confident_errors']}
- validácia: emulované {S['validation']['_emulation_rate'][0]:.2%}, na hybrid {S['validation']['_hybrid_rate'][0]:.2%}

## Validácia
{block('validation')}
{holdout}
## Krivka rozpočtu emulácie (test, priemer cez seedy)
{_tbl(curve) if curve is not None else '_bez krivky_'}

## Výpočtové nároky
Emulácia (Speakeasy) sa nedá zmerať (dataset neobsahuje PE súbory). **Predpoklad** {emu_s:.0f} s na súbor
(limit z `speakeasy-config.json`): kaskáda B ≈ {emu * emu_s:.1f} s na súbor v priemere, dynamický/hybridný model
a kaskáda A {emu_s:.0f} s (emulujú každý súbor).

{cost_txt}

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
"""
    (out / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--runs-root", default=None)
    a = ap.parse_args()
    main(a.config, Path(a.runs_root) if a.runs_root else RUNS_DIR)
