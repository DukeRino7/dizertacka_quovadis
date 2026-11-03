"""Vyhodnotenie kaskády z uložených predikcií (bez opätovného spúšťania modelov).

Kaskáda: statický a dynamický model rozhodnú pri svojich prahoch z validácie; ak sa zhodnú, rozhodnutie je
konečné, inak rozhodne hybridný model (pri svojom prahu z validácie).

Porovnanie na rovnakých vzorkách s: hybridom na každej vzorke, samostatným statickým a dynamickým modelom
a neskorou fúziou (mean, stacking). Výpočtové nároky z benchmarkov komponentov:
    kaskáda ≈ statický + dynamický + podiel eskalácií × hybrid      (odhad; meranie celej kaskády zvlášť)

    .venv\\Scripts\\python.exe -m src.cascade.evaluate --config configs/cascade/<variant>.yaml
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
from src.models.hybrid.late_fusion import fuse
from .components import Component

DEC_METRICS = ["accuracy", "balanced_accuracy", "precision", "recall_tpr", "fpr", "f1", "mcc"]


def _merge(comps: dict, split: str, seed: int) -> pd.DataFrame:
    base = None
    for role, c in comps.items():
        d = c.scores(split, seed).rename(columns={"score": f"s_{role}"})
        base = d if base is None else base.merge(d[["sha256", f"s_{role}"]], on="sha256", validate="one_to_one")
    return base


def evaluate_seed(comps: dict, seed: int, target_fpr: float) -> dict:
    V, T = _merge(comps, "validation", seed), _merge(comps, "test", seed)
    thr = {r: comps[r].threshold(seed) for r in comps}
    out = {"seed": seed, "thresholds": thr, "n": {"validation": len(V), "test": len(T)}}

    # neskorá fúzia (prah z validácie pre FPR <= target)
    fus = {}
    for m in ("mean", "stacking"):
        sv, st = fuse(m, (V["s_static"].to_numpy(), V["s_dynamic"].to_numpy()),
                      (T["s_static"].to_numpy(), T["s_dynamic"].to_numpy()), V["label"].to_numpy(), seed)
        fus[m] = (sv, st, threshold_for_fpr(V["label"].to_numpy(), sv, target_fpr))

    for split, D in (("validation", V), ("test", T)):
        y = D["label"].to_numpy()
        dec = {r: (D[f"s_{r}"].to_numpy() >= thr[r]).astype(int) for r in comps}
        agree = dec["static"] == dec["dynamic"]
        final = np.where(agree, dec["static"], dec["hybrid"])
        res = {"approaches": {}}
        res["approaches"]["cascade"] = at_threshold(y, final.astype(float), 0.5)
        for r in comps:
            res["approaches"][f"{r}_only"] = at_threshold(y, D[f"s_{r}"].to_numpy(), thr[r])
        for m, (sv, st, t) in fus.items():
            res["approaches"][f"late_fusion_{m}"] = at_threshold(y, sv if split == "validation" else st, t)

        esc = ~agree
        wrong_agree = agree & (dec["static"] != y)
        res["cascade"] = {
            "escalation_rate": float(esc.mean()),
            "n_escalated": int(esc.sum()),
            "agreement_error_rate": float(wrong_agree.sum() / max(agree.sum(), 1)),   # chyby pri zhode / zhody
            "n_agreement_errors": int(wrong_agree.sum()),
            "agreement_fp": int((wrong_agree & (y == 0)).sum()), "agreement_fn": int((wrong_agree & (y == 1)).sum()),
            "escalated_accuracy": {  # kto by na eskalovaných vzorkách rozhodol správne
                "hybrid": float((dec["hybrid"][esc] == y[esc]).mean()) if esc.any() else None,
                "static": float((dec["static"][esc] == y[esc]).mean()) if esc.any() else None,
                "dynamic": float((dec["dynamic"][esc] == y[esc]).mean()) if esc.any() else None,
            },
            "per_family": (pd.DataFrame({"family": D["family"], "esc": esc, "err_agree": wrong_agree,
                                         "wrong": final != y})
                           .groupby("family").agg(n=("esc", "size"), escalation_rate=("esc", "mean"),
                                                  agreement_errors=("err_agree", "sum"), error_rate=("wrong", "mean"))
                           .reset_index().to_dict("records")),
        }
        out[split] = res
    # zero-day: januárové vzorky vynechanej rodiny (iba malvér) -> TPR
    if all(c.has_split("holdout", seed) for c in comps.values()):
        H = _merge(comps, "holdout", seed)
        dec = {r: (H[f"s_{r}"].to_numpy() >= thr[r]).astype(int) for r in comps}
        final = np.where(dec["static"] == dec["dynamic"], dec["static"], dec["hybrid"])
        out["holdout"] = {"n": len(H), "tpr": {"cascade": float(final.mean()), **{f"{r}_only": float(dec[r].mean()) for r in comps}},
                          "escalation_rate": float((dec["static"] != dec["dynamic"]).mean())}
    return out


def cost_table(comps: dict, esc_rate: float) -> pd.DataFrame | None:
    c = {r: comps[r].cost() for r in comps}
    if any(v is None for v in c.values()):
        return None
    rows = []
    for key, label in [("cpu_ms_batch", "CPU čas ms/vz. (dávka)"), ("cpu_ms_single", "CPU čas ms/vz. (1 vz.)"),
                       ("latency_ms", "latencia ms (1 vz., postupne)")]:
        s, d, h = c["static"][key], c["dynamic"][key], c["hybrid"][key]
        rows.append({"meranie": label, "statický": s, "dynamický": d, "hybrid na každej vzorke": h,
                     "neskorá fúzia": s + d, "kaskáda (odhad)": s + d + esc_rate * h})
    return pd.DataFrame(rows)


def main(config_path: str, runs_root: Path = RUNS_DIR):
    cfg = load_config(config_path)
    comps = {r: Component(cfg["components"][r], runs_root) for r in ("static", "dynamic", "hybrid")}
    seeds = sorted(set.intersection(*(set(c.seeds) for c in comps.values())))
    target = load_config(cfg.get("protocol", "configs/protocol.yaml"))["thresholds"]["target_fpr"]
    per_seed = [evaluate_seed(comps, s, target) for s in seeds]

    out = runs_root / "cascade" / cfg["name"] / datetime.now().strftime("%Y%m%d-%H%M%S")
    (out / "plots").mkdir(parents=True)
    summary = {}
    for split in ("validation", "test"):
        names = per_seed[0][split]["approaches"].keys()
        summary[split] = {a: {m: (float(np.mean([p[split]["approaches"][a][m] for p in per_seed])),
                                  float(np.std([p[split]["approaches"][a][m] for p in per_seed], ddof=1)) if len(per_seed) > 1 else 0.0)
                              for m in DEC_METRICS} for a in names}
        summary[split]["_escalation_rate"] = float(np.mean([p[split]["cascade"]["escalation_rate"] for p in per_seed]))
    costs = cost_table(comps, summary["test"]["_escalation_rate"])
    write_json({"created": now_iso(), "config": cfg, "git": git_info(),
                "components": {r: rel(c.run) for r, c in comps.items()}, "seeds": seeds,
                "summary": summary, "per_seed": per_seed,
                "costs": costs.to_dict("records") if costs is not None else None}, out / "metrics.json")
    plot_compare(summary["test"], out / "plots" / "approaches_test.png")
    plot_family(per_seed[0]["test"]["cascade"]["per_family"], out / "plots" / "escalation_by_family.png")
    write_readme(out, cfg, comps, seeds, summary, per_seed, costs)
    print(f"Kaskáda vyhodnotená: {rel(out)}")
    return out


LABELS = {"cascade": "kaskáda", "hybrid_only": "hybrid (každá vzorka)", "static_only": "statický",
          "dynamic_only": "dynamický", "late_fusion_mean": "neskorá fúzia (priemer)",
          "late_fusion_stacking": "neskorá fúzia (stacking)"}


def plot_compare(S, path):
    names = [a for a in LABELS if a in S]
    fig, ax = P._fig(8, 4.6)
    y = np.arange(len(names))[::-1]
    # bodový graf (nie stĺpce): os nezačína nulou, stĺpce by rozdiely opticky zveličili
    for k, (m, lab, col, mk) in enumerate([("f1", "F1", P.SPLIT_COLOR["test"], "o"),
                                           ("recall_tpr", "TPR (detekcia)", P.SPLIT_COLOR["train"], "D")]):
        ax.scatter([S[a][m][0] for a in names], y + (0.12 - 0.24 * k), s=70, marker=mk, color=col,
                   edgecolor=P.SURFACE, linewidth=1.5, label=lab, zorder=3)
    lo = min(S[a][m][0] for a in names for m in ("f1", "recall_tpr"))
    ax.set_xlim(max(0, lo - 0.03), 1.0)
    ax.set_ylim(-0.6, len(names) - 0.4)
    ax.set_yticks(y, [LABELS[a] for a in names])
    P._style(ax, "Porovnanie prístupov na teste (prahy z validácie)", "hodnota metriky", "", grid="x")
    ax.legend(frameon=False, labelcolor=P.INK2, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
    P._save(fig, path)


def plot_family(rows, path):
    d = pd.DataFrame(rows)
    fams = ["benign"] + sorted(f for f in d["family"] if f != "benign")
    d = d.set_index("family").loc[fams]
    fig, ax = P._fig(7.5, 4.6)
    y = np.arange(len(fams))[::-1]
    ax.barh(y, d["escalation_rate"] * 100, height=0.6, color=P.SPLIT_COLOR["validation"])
    for yi, v in zip(y, d["escalation_rate"] * 100):
        ax.text(v, yi, f"  {v:.1f} %", va="center", color=P.INK, fontsize=9)
    ax.set_yticks(y, fams)
    P._style(ax, "Podiel eskalácií na hybridný model podľa rodiny (test, seed 0)", "eskalované vzorky [%]", "", grid="x")
    P._save(fig, path)


def write_readme(out, cfg, comps, seeds, S, per_seed, costs):
    def row(a, split):
        return "| " + LABELS[a] + " | " + " | ".join(f"{S[split][a][m][0]:.4f} ± {S[split][a][m][1]:.4f}" for m in DEC_METRICS) + " |"
    head = "| prístup | " + " | ".join(DEC_METRICS) + " |\n|---|" + "---|" * len(DEC_METRICS)
    names = [a for a in LABELS if a in S["test"]]
    c0 = per_seed[0]["test"]["cascade"]
    cost_txt = "_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._"
    if costs is not None:
        cols = list(costs.columns)
        cost_txt = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n" + "\n".join(
            "| " + " | ".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in r.values()) + " |" for r in costs.to_dict("records"))
    text = f"""# Kaskáda `{cfg['name']}` – beh `{out.name}`

> Generované `src/cascade/evaluate.py` ({now_iso()}). Seedy: {seeds}; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
""" + "\n".join(f"| {r} | `{rel(c.run)}` |" for r, c in comps.items()) + f"""

## Test
{head}
{chr(10).join(row(a, 'test') for a in names)}

## Validácia
{head}
{chr(10).join(row(a, 'validation') for a in names)}

## Správanie kaskády (test, seed {seeds[0]})
- podiel eskalácií na hybrid: **{c0['escalation_rate']:.2%}** ({c0['n_escalated']} vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **{c0['n_agreement_errors']}**
  ({c0['agreement_error_rate']:.3%} zo zhôd; FP {c0['agreement_fp']}, FN {c0['agreement_fn']})
- úspešnosť na eskalovaných vzorkách: hybrid {c0['escalated_accuracy']['hybrid']}, statický {c0['escalated_accuracy']['static']},
  dynamický {c0['escalated_accuracy']['dynamic']}  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
{cost_txt}

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
"""
    (out / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--runs-root", default=None)
    a = ap.parse_args()
    main(a.config, Path(a.runs_root) if a.runs_root else RUNS_DIR)
