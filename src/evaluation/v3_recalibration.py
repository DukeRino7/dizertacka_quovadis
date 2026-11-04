r"""V3 – C (docs/12, bod 3): prekalibrovanie prahu na nových neškodných súboroch – samostatný scenár.

Neškodné súbory aprílového testu sa náhodne (podľa skupín identických EMBER vektorov) rozdelia na kalibračnú
a hodnotiacu časť; malvér ide celý do hodnotenia (kalibrácia ho nevidí). Prah každého modelu a každého komponentu
kaskády sa nastaví na FPR 1 % na kalibračnej časti; eskalácia kaskád B (pásmo / rozpočet) ostáva z validácie.
Porovnanie na tej istej hodnotiacej časti: prahy z validácie („pôvodný“) vs. prekalibrované („prekalibrovaný“).
Veľkosti kalibračnej časti 1 / 5 / 20 % neškodných, 10 náhodných rozdelení, seedy 0–2.

Iba z uložených predikcií (runs_final, runs_v2/lofo, runs_v3), bez tréningu.

    .venv\Scripts\python.exe -m src.evaluation.v3_recalibration --v1 runs_final --v2 runs_v2 --v3 runs_v3
"""
import argparse
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.cascade.components import Component
from src.cascade.evaluate_b import band, decide, logit
from src.cascade.specialist import spec_threshold
from src.common.paths import INDEX_DIR, PROJECT_ROOT

SIZES = [0.01, 0.05, 0.20]
N_SPLITS = 10
TARGET = 0.01
SINGLES = {"static": "static/lightgbm", "dynamic": "dynamic/lightgbm", "hybrid": "hybrid/lightgbm", "two_branch": "hybrid/two_branch"}
STUDENTS = {"st_static": "students_static/mlp_kd", "st_dynamic": "students_dynamic/mlp_kd"}
LABELS = {"static": "statický LightGBM", "dynamic": "dynamický LightGBM", "hybrid": "hybrid LightGBM",
          "two_branch": "hybrid dvojvetvová sieť", "A_main": "kaskáda A-main", "A_baselines": "kaskáda A-baselines",
          "B_main": "kaskáda B-main", "B_baselines": "kaskáda B-baselines (rozpočet 10 %)",
          "v3_spec": "kaskáda V3 špecialista (hybrid)", "v3_spec_dyn": "kaskáda V3 špecialista (dynamika)"}
CASCADES = ["A_main", "A_baselines", "B_main", "B_baselines", "v3_spec", "v3_spec_dyn"]


def thr_benign(scores: np.ndarray, target: float = TARGET) -> float:
    """Najnižší prah, pri ktorom je FPR na daných neškodných súboroch ≤ target."""
    s = np.sort(scores)[::-1]
    allowed = int(np.floor(target * len(s) + 1e-9))
    return float(np.nextafter(s[allowed], np.inf)) if allowed < len(s) else 0.0


def calibration_splits(test_meta: pd.DataFrame) -> dict:
    """(veľkosť, číslo rozdelenia) -> boolovská maska kalibračných neškodných súborov v poradí test_meta."""
    idx = pd.read_parquet(INDEX_DIR / "samples.parquet", columns=["sha256", "feature_group"]).drop_duplicates("sha256")
    g = test_meta[["sha256"]].merge(idx, on="sha256", how="left")["feature_group"].to_numpy()
    ben = test_meta["label"].to_numpy() == 0
    groups = np.unique(g[ben])
    n_ben = int(ben.sum())
    out = {}
    for size in SIZES:
        for k in range(N_SPLITS):
            rng = np.random.default_rng(10_000 * k + int(round(size * 1000)))
            chosen, count = [], 0
            sizes = pd.Series(g[ben]).value_counts()
            for grp in rng.permutation(groups):
                if count >= round(size * n_ben):
                    break
                chosen.append(grp); count += int(sizes[grp])
            out[(size, k)] = ben & np.isin(g, chosen)
    return out


class Setting:
    """Predikcie komponentov jedného nastavenia (časový test alebo jedna vynechaná rodina) pre jeden seed."""

    def __init__(self, comp_root: Path, v3_root: Path | None, family: str | None):
        self.comp_root, self.v3_root, self.family = comp_root, v3_root, family
        specs = {**SINGLES, **STUDENTS}
        self.comps = {k: Component(v, comp_root) for k, v in specs.items()}
        self.spec_runs = {}
        if v3_root is not None:
            for v in ("v3_spec", "v3_spec_dyn"):
                runs = sorted((v3_root / "cascade" / v).glob("*/metrics.json"))
                if runs:
                    self.spec_runs[v] = runs[-1].parent
        self.seeds = sorted(set.intersection(*(set(c.seeds) for c in self.comps.values())))

    def load(self, seed: int, order: np.ndarray) -> dict:
        def get(c, split, sha):
            return c.scores(split, seed).set_index("sha256")["score"].reindex(sha).to_numpy()
        D = {"thr": {k: c.threshold(seed) for k, c in self.comps.items()}}
        for split in ("validation", "test"):
            sha = order if split == "test" else self.comps["static"].scores("validation", seed)["sha256"].to_numpy()
            D[split] = {k: get(c, split, sha) for k, c in self.comps.items()}
            if split == "validation":
                D["y_val"] = self.comps["static"].scores("validation", seed)["label"].to_numpy()
        # pásmo kaskády B-main a hranica rozpočtu 10 % kaskády B-baselines – z validácie (nemenia sa)
        D["band"] = band(D["validation"]["st_static"], D["y_val"], 0.001, 0.01)
        dist_v = np.abs(logit(D["validation"]["static"]) - logit(D["thr"]["static"]))
        D["bb_esc"] = np.abs(logit(D["test"]["static"]) - logit(D["thr"]["static"])) <= np.quantile(dist_v, 0.1)
        D["spec"] = {}
        for v, run in self.spec_runs.items():
            m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
            ps = next((p for p in m["per_seed"] if p["seed"] == seed), None)
            if ps is None:
                continue
            p = pd.read_parquet(run / "predictions" / f"test_seed{seed}.parquet").set_index("sha256").reindex(order)
            D["spec"][v] = {"score": p["score"].to_numpy(), "esc": p["escalated_main"].to_numpy(bool),
                            "thr": ps["budgets"][str(m["config"]["main_budget"])]["spec_threshold"]}
        return D


def decisions(D: dict, thr: dict, spec_thr: dict) -> dict:
    """Rozhodnutia všetkých prístupov na teste pri daných prahoch (thr: komponent -> prah)."""
    T = D["test"]
    dec = {k: T[k] >= thr[k] for k in T}
    out = {k: dec[k] for k in SINGLES}
    out["A_baselines"] = np.where(dec["static"] == dec["dynamic"], dec["static"], dec["hybrid"])
    out["A_main"] = np.where(dec["st_static"] == dec["st_dynamic"], dec["st_static"], dec["hybrid"])
    lo, hi = D["band"]
    Bm = pd.DataFrame({"s_static": T["st_static"], "s_dynamic": T["st_dynamic"], "s_hybrid": T["hybrid"]})
    s = T["st_static"]
    out["B_main"] = decide(Bm, (s >= lo) & (s < hi), {"static": thr["st_static"], "dynamic": thr["st_dynamic"],
                                                      "hybrid": thr["hybrid"]}, lo, hi, "dynamic")["final"].astype(bool)
    Bb = pd.DataFrame({"s_static": T["static"], "s_dynamic": T["dynamic"], "s_hybrid": T["hybrid"]})
    out["B_baselines"] = decide(Bb, D["bb_esc"], {k: thr[k] for k in ("static", "dynamic", "hybrid")},
                                thr["static"], thr["static"], "dynamic")["final"].astype(bool)
    for v, sp in D["spec"].items():
        out[v] = np.where(sp["esc"], sp["score"] >= spec_thr[v], dec["static"])
    return out


def recalibrated(D: dict, calib: np.ndarray) -> tuple[dict, dict]:
    T = D["test"]
    thr = {k: thr_benign(T[k][calib]) for k in T}
    spec_thr = {}
    for v, sp in D["spec"].items():
        n = int(calib.sum())
        spec_thr[v] = spec_threshold(np.zeros(n, int), T["static"][calib] >= thr["static"], sp["esc"][calib],
                                     sp["score"][calib], TARGET)
    return thr, spec_thr


def run(v1: Path, v2: Path, v3: Path, families: list[str]) -> pd.DataFrame:
    settings = [("časový", v1, v3 / "full" if (v3 / "full").exists() else None, None)]
    settings += [(f, v2 / "lofo" / f, v3 / "lofo" / f if (v3 / "lofo" / f).exists() else None, f) for f in families]
    recs, splits = [], None
    for name, comp_root, v3_root, fam in settings:
        st = Setting(comp_root, v3_root, fam)
        test_meta = st.comps["static"].scores("test", st.seeds[0])[["sha256", "family", "label"]]
        if splits is None:
            splits, order = calibration_splits(test_meta), test_meta["sha256"].to_numpy()
        tm = test_meta.set_index("sha256").reindex(order)
        y, fams = tm["label"].to_numpy(), tm["family"].to_numpy()
        fm = (fams == fam) & (y == 1) if fam else None
        print(f"{name}: seedy {st.seeds}, kaskády V3: {sorted(st.spec_runs)}", flush=True)
        for seed in st.seeds:
            D = st.load(seed, order)
            orig = decisions(D, D["thr"], {v: sp["thr"] for v, sp in D["spec"].items()})
            for (size, k), calib in splits.items():
                ev = ~calib
                new = decisions(D, *recalibrated(D, calib))
                for mode, dd in (("pôvodný", orig), ("prekalibrovaný", new)):
                    for model, d in dd.items():
                        recs.append({"setting": name, "seed": seed, "size": size, "split": k, "model": model, "mode": mode,
                                     "tpr": float(d[ev & (y == 1)].mean()), "fpr": float(d[ev & (y == 0)].mean()),
                                     "tpr_family": float(d[fm].mean()) if fam else np.nan})
    return pd.DataFrame(recs)


def fmt(m, s):
    return f"{m:.4f} ± {s:.4f}"


def report(df: pd.DataFrame, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "recalibration.csv", index=False)
    zd = df[df.setting != "časový"]
    fams = sorted(zd.setting.unique())
    L = ["# V3 – C: prekalibrovanie prahu na nových neškodných súboroch (samostatný scenár)", "",
         "> Generované `src/evaluation/v3_recalibration.py`. Plán: `docs/12_plan_v3.md`, bod 3. Kalibrácia používa iba",
         "> neškodné súbory aprílového testu (kalibračná časť), hodnotí sa na zvyšku testu; malvér kalibrácia nevidí.",
         f"> {N_SPLITS} náhodných rozdelení × seedy, hodnota = priemer ± sm. odchýlka cez rozdelenia a seedy.",
         "> „pôvodný“ = prahy z validácie na tej istej hodnotiacej časti. Hlavné výsledky V1–V3 sa týmto nemenia.", ""]

    def table(sub: pd.DataFrame, tpr_col: str, title: str):
        # najprv priemer cez rodiny (ak sú), potom priemer ± sd cez rozdelenia a seedy
        cols = list(dict.fromkeys([tpr_col, "fpr", "tpr"]))
        a = sub.groupby(["size", "split", "seed", "model", "mode"])[cols].mean().reset_index()
        g = a.groupby(["size", "model", "mode"])[cols].agg(["mean", "std"])
        rows = []
        for size in SIZES:
            for model in LABELS:
                if (size, model, "pôvodný") not in g.index:
                    continue
                o, n = g.loc[(size, model, "pôvodný")], g.loc[(size, model, "prekalibrovaný")]
                rows.append(f"| {size:.0%} | {LABELS[model]} | {fmt(o[(tpr_col, 'mean')], o[(tpr_col, 'std')])} | "
                            f"{fmt(n[(tpr_col, 'mean')], n[(tpr_col, 'std')])} | {fmt(o[('fpr', 'mean')], o[('fpr', 'std')])} | "
                            f"{fmt(n[('fpr', 'mean')], n[('fpr', 'std')])} |")
        return [f"## {title}", "", "| kalibrácia (podiel neškodných) | prístup | TPR pôvodný | TPR prekalibrovaný | FPR pôvodný | FPR prekalibrovaný |",
                "|---|---|---|---|---|---|"] + rows + [""], a

    t_lines, ta = table(df[df.setting == "časový"], "tpr", "1. Časový test – TPR všetkého malvéru")
    L += t_lines
    za = None
    if len(zd):
        z_lines, za = table(zd, "tpr_family", f"2. Zero-day – TPR vynechanej rodiny (priemer cez {len(fams)} rodín: {', '.join(fams)})")
        L += z_lines

    # téza 2 v scenári C: kaskády vs. prekalibrovaný statický a dynamický model (rovnaké kritérium ako docs/09)
    L += ["## 3. Téza 2 v scenári C (FPR < statický aj dynamický, TPR všetkého malvéru ≥ statický − 1 p. b.)", "",
          "| kalibrácia | test | kaskáda | FPR | TPR | FPR statický | FPR dynamický | TPR statický | spĺňa |", "|---|---|---|---|---|---|---|---|---|"]
    for label, a in (("časový", ta), ("zero-day", za)):
        if a is None:
            continue
        m = a[a["mode"] == "prekalibrovaný"].groupby(["size", "model"])[["fpr", "tpr"]].mean()
        for size in SIZES:
            s, d = m.loc[(size, "static")], m.loc[(size, "dynamic")]
            for c in CASCADES:
                if (size, c) not in m.index:
                    continue
                r = m.loc[(size, c)]
                ok = r.fpr < s.fpr and r.fpr < d.fpr and r.tpr >= s.tpr - 0.01
                L.append(f"| {size:.0%} | {label} | {LABELS[c]} | {r.fpr:.4f} | {r.tpr:.4f} | {s.fpr:.4f} | {d.fpr:.4f} | {s.tpr:.4f} | {'áno' if ok else 'nie'} |")
    L.append("")
    (out / "RECALIBRATION.md").write_text("\n".join(L), encoding="utf-8")
    print(f"Scenár C: {out / 'RECALIBRATION.md'}")


def main(v1: Path, v2: Path, v3: Path, families: list[str], out: Path):
    report(run(v1, v2, v3, families), out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", type=Path, default=Path("runs_final"))
    ap.add_argument("--v2", type=Path, default=Path("runs_v2"))
    ap.add_argument("--v3", type=Path, default=Path("runs_v3"))
    ap.add_argument("--families", nargs="*", default=["backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan"])
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    main(a.v1, a.v2, a.v3, a.families, a.out or a.v3 / "comparison" / "v3")
