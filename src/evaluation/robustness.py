r"""Overenie robustnosti (docs/16): R1 štatistická významnosť hlavných tvrdení, R2 citlivosť na chybu emulácie.

Iba z uložených predikcií (runs_final, runs_v2/lofo, runs_v3), prahy z validácie. R1: párový bootstrap testovacích
súborov (stratifikovane podľa triedy), metrika = priemer cez seedy (a v zero-day cez rodiny), 95 % percentilový interval
rozdielu. Body 7 a 8 z párových rozdielov scenára C (recalibration.csv). R2: to isté iba na súboroch s úspešnou emuláciou.

    .venv\Scripts\python.exe -m src.evaluation.robustness --v1 runs_final --v2 runs_v2 --v3 runs_v3
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.cascade.components import Component
from src.evaluation.v2_analysis import emulation_subsets
from src.evaluation.v3_recalibration import Setting, decisions

FAMS = ["backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan"]
B = 2000
TOL = 0.01
LAB = {"static": "statický LightGBM", "dynamic": "dynamický LightGBM", "hybrid": "hybrid LightGBM",
       "two_branch": "dvojvetvová sieť", "kd_twobranch": "študent z dvojvetvovej siete", "A_main": "kaskáda A-main",
       "A_baselines": "kaskáda A-baselines", "B_main": "kaskáda B-main", "B_baselines": "kaskáda B-baselines (10 %)",
       "v3_spec": "špecialista V3", "S_or_D": "statický ALEBO dynamický (horná hranica)"}


def load_all(v1: Path, v2: Path, v3: Path) -> tuple[dict, pd.DataFrame]:
    """Rozhodnutia všetkých prístupov: setting -> seed -> {prístup: bool vektor}; spoločné poradie testu."""
    settings = [("časový", v1, v3 / "full", None)] + [(f, v2 / "lofo" / f, v3 / "lofo" / f, f) for f in FAMS]
    dec, scores, meta = {}, {}, None
    for name, comp_root, v3_root, fam in settings:
        st = Setting(comp_root, v3_root if v3_root.exists() else None, fam)
        if meta is None:
            meta = st.comps["static"].scores("test", st.seeds[0])[["sha256", "family", "label"]].reset_index(drop=True)
        order = meta["sha256"].to_numpy()
        kd = Component("students_static/mlp_kd_twobranch", comp_root) if fam else None
        dec[name], scores[name] = {}, {}
        for seed in st.seeds:
            D = st.load(seed, order)
            d = decisions(D, D["thr"], {v: sp["thr"] for v, sp in D["spec"].items()})
            d["S_or_D"] = d["static"] | d["dynamic"]
            if kd is not None:
                s = kd.scores("test", seed).set_index("sha256")["score"].reindex(order).to_numpy()
                d["kd_twobranch"] = s >= kd.threshold(seed)
            dec[name][seed] = d
            scores[name][seed] = {"static": D["test"]["static"], "dynamic": D["test"]["dynamic"]}
        print(f"{name}: načítané seedy {st.seeds}", flush=True)
    return {"dec": dec, "scores": scores}, meta


def boot_weights(y: np.ndarray, mask: np.ndarray, rng) -> np.ndarray:
    """B × N matica počtov výberu (stratifikovaný bootstrap v rámci masky; mimo masky 0)."""
    W = np.zeros((B, len(y)), dtype=np.int32)
    for cls in (0, 1):
        idx = np.flatnonzero(mask & (y == cls))
        draws = rng.integers(0, len(idx), size=(B, len(idx)))
        for b in range(B):
            W[b] += np.bincount(idx[draws[b]], minlength=len(y)).astype(np.int32)
    return W


def metrics_boot(W, d, sel_mal, sel_ben):
    """TPR (na vybranom malvéri) a FPR (na vybraných neškodných) v každom bootstrap opakovaní + bodový odhad."""
    d = d.astype(np.int32)
    tm, tb = W[:, sel_mal], W[:, sel_ben]
    tpr = (tm @ d[sel_mal]) / np.maximum(tm.sum(1), 1)
    fpr = (tb @ d[sel_ben]) / np.maximum(tb.sum(1), 1)
    return tpr, fpr, d[sel_mal].mean(), d[sel_ben].mean()


def compare(ctx, meta, W, setting_names, a, b, metric, subset=None):
    """Rozdiel metriky a − b (priemer cez seedy a nastavenia) s bootstrap intervalom."""
    y, fam = meta["label"].to_numpy(), meta["family"].to_numpy()
    sub = np.ones(len(y), bool) if subset is None else subset
    diffs, points = [], []
    for name in setting_names:
        for seed, d in ctx["dec"][name].items():
            if a not in d or b not in d:
                continue
            mal = (y == 1) & sub & ((fam == name) if metric == "tpr_family" else True)
            ben = (y == 0) & sub
            ta, fa, pta, pfa = metrics_boot(W, d[a], mal, ben)
            tb_, fb, ptb, pfb = metrics_boot(W, d[b], mal, ben)
            if metric == "fpr":
                diffs.append(fa - fb); points.append(pfa - pfb)
            else:
                diffs.append(ta - tb_); points.append(pta - ptb)
    D = np.mean(diffs, axis=0)
    return float(np.mean(points)), float(np.percentile(D, 2.5)), float(np.percentile(D, 97.5))


def verdict(kind, est, lo, hi):
    if kind == "lower":
        return "áno" if hi < 0 else "nie"
    if kind == "higher":
        return "áno" if lo > 0 else "nie"
    if kind == "noninf":
        return "áno" if lo > -TOL else "nie"
    if kind == "equiv":
        return "áno" if (lo > -TOL and hi < TOL) else "nie"
    raise ValueError(kind)


R1 = [  # (č., tvrdenie, a, b, metrika, druh, nastavenia)
    (1, "A-baselines má nižšie FPR ako statický", "A_baselines", "static", "fpr", "lower", "both"),
    (1, "A-baselines: TPR všetkého malvéru nie horšie ako statický", "A_baselines", "static", "tpr", "noninf", "both"),
    (2, "B-baselines (10 %) má nižšie FPR ako statický", "B_baselines", "static", "fpr", "lower", "both"),
    (2, "B-baselines (10 %): TPR nie horšie ako statický", "B_baselines", "static", "tpr", "noninf", "both"),
    (3, "B-baselines (10 %): TPR nie horšie ako hybrid", "B_baselines", "hybrid", "tpr", "noninf", "both"),
    (3, "B-baselines (10 %) má nižšie FPR ako hybrid", "B_baselines", "hybrid", "fpr", "lower", "both"),
    (4, "A-main: TPR vynechanej rodiny horšie ako statický", "A_main", "static", "tpr_family", "lower", "zd"),
    (4, "B-main: TPR vynechanej rodiny horšie ako statický", "B_main", "static", "tpr_family", "lower", "zd"),
    (5, "hybrid = statický (TPR všetkého malvéru)", "hybrid", "static", "tpr", "equiv", "both"),
    (5, "hybrid = statický (TPR vynechanej rodiny)", "hybrid", "static", "tpr_family", "equiv", "zd"),
    (6, "študent z dvojvetvovej siete = učiteľ (TPR vynechanej rodiny)", "kd_twobranch", "two_branch", "tpr_family", "equiv", "zd"),
]
R2_EXTRA = [  # iba citlivosť na emuláciu
    ("statický ALEBO dynamický − statický (horná hranica kombinácie)", "S_or_D", "static", "tpr_family", "zd"),
    ("hybrid − statický", "hybrid", "static", "tpr_family", "zd"),
    ("špecialista V3 − statický", "v3_spec", "static", "tpr_family", "zd"),
    ("špecialista V3 − statický (FPR)", "v3_spec", "static", "fpr", "zd"),
]


def recal_pairs(v3: Path) -> list[dict]:
    """Body 7 a 8: párové rozdiely zo scenára C (cez rozdelenia × seedy)."""
    df = pd.read_csv(v3 / "comparison" / "v3" / "recalibration.csv")
    out = []
    for test, sub, col in (("zero-day", df[df.setting != "časový"], "tpr_family"), ("časový", df[df.setting == "časový"], "tpr")):
        g = sub.groupby(["size", "split", "seed", "model", "mode"])[[col, "fpr"]].mean().reset_index()
        for size in (0.05, 0.20):
            x = g[g["size"] == size].set_index(["split", "seed", "model", "mode"])
            for label, (ma, mo_a), (mb, mo_b), met in [
                ("7: špecialista − statický pri prekalibrovanom prahu (TPR)", ("v3_spec", "prekalibrovaný"), ("static", "prekalibrovaný"), col),
                ("7: špecialista − statický pri prekalibrovanom prahu (FPR)", ("v3_spec", "prekalibrovaný"), ("static", "prekalibrovaný"), "fpr"),
                ("8: statický prekalibrovaný − pôvodný (TPR)", ("static", "prekalibrovaný"), ("static", "pôvodný"), col),
                ("8: statický prekalibrovaný − pôvodný (FPR)", ("static", "prekalibrovaný"), ("static", "pôvodný"), "fpr")]:
                a = x.xs((ma, mo_a), level=("model", "mode"))[met]
                b = x.xs((mb, mo_b), level=("model", "mode"))[met]
                d = (a - b).dropna()
                out.append({"tvrdenie": label, "test": test, "kalibrácia": f"{size:.0%}", "rozdiel": float(d.mean()),
                            "2,5 %": float(np.percentile(d, 2.5)), "97,5 %": float(np.percentile(d, 97.5)), "n párov": len(d)})
    return out


def pp(v):
    return f"{v * 100:+.2f}"


def main(v1: Path, v2: Path, v3: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    ctx, meta = load_all(v1, v2, v3)
    y, fam = meta["label"].to_numpy(), meta["family"].to_numpy()
    emu = emulation_subsets().reindex(meta["sha256"]).to_numpy()
    ok = emu == "emulácia ok"
    rng = np.random.default_rng(20261107)
    print("bootstrap ...", flush=True)
    W_all = boot_weights(y, np.ones(len(y), bool), rng)
    W_ok = boot_weights(y, ok, rng)

    def sets(which):
        return {"both": [("časový", ["časový"]), ("zero-day", FAMS)], "zd": [("zero-day", FAMS)]}[which]

    rows = []
    for n, claim, a, b, met, kind, which in R1:
        for test, names in sets(which):
            for subset_name, W, sub in (("všetky", W_all, None), ("emulácia ok", W_ok, ok)):
                est, lo, hi = compare(ctx, meta, W, names, a, b, met, sub)
                rows.append({"č.": n, "tvrdenie": claim, "test": test, "súbory": subset_name, "rozdiel [p. b.]": pp(est),
                             "95 % IS": f"{pp(lo)} až {pp(hi)}", "potvrdené": verdict(kind, est, lo, hi),
                             "_est": est, "_lo": lo, "_hi": hi})
    r1 = pd.DataFrame(rows)
    r1.drop(columns=[c for c in r1 if c.startswith("_")]).to_csv(out / "r1_bootstrap.csv", index=False)

    # R2: úrovne na podskupine s úspešnou emuláciou (zero-day, priemer cez rodiny) + horná hranica a AUC
    lev = []
    for subset_name, sub in (("všetky", np.ones(len(y), bool)), ("emulácia ok", ok)):
        for key in ("static", "dynamic", "hybrid", "S_or_D", "A_baselines", "B_baselines", "v3_spec"):
            tf, fp = [], []
            for f in FAMS:
                for seed, d in ctx["dec"][f].items():
                    if key in d:
                        m = (fam == f) & (y == 1) & sub
                        tf.append(d[key][m].mean()); fp.append(d[key][(y == 0) & sub].mean())
            lev.append({"súbory": subset_name, "prístup": LAB[key], "TPR vynech. rodiny": np.mean(tf), "FPR": np.mean(fp)})
        for key in ("static", "dynamic"):
            aucs = []
            for f in FAMS:
                for seed, s in ctx["scores"][f].items():
                    sel = (((fam == f) & (y == 1)) | (y == 0)) & sub
                    aucs.append(roc_auc_score(y[sel], s[key][sel]))
            lev.append({"súbory": subset_name, "prístup": f"ROC-AUC {LAB[key]}", "TPR vynech. rodiny": np.mean(aucs), "FPR": np.nan})
    lev = pd.DataFrame(lev)
    lev.to_csv(out / "r2_levels.csv", index=False)
    r2 = []
    for claim, a, b, met, which in R2_EXTRA:
        for subset_name, W, sub in (("všetky", W_all, None), ("emulácia ok", W_ok, ok)):
            est, lo, hi = compare(ctx, meta, W, FAMS, a, b, met, sub)
            r2.append({"porovnanie": claim, "súbory": subset_name, "rozdiel [p. b.]": pp(est), "95 % IS": f"{pp(lo)} až {pp(hi)}",
                       "_est": est, "_hi": hi})
    r2 = pd.DataFrame(r2)
    rc = pd.DataFrame(recal_pairs(v3))
    rc.to_csv(out / "r1_recalibration_pairs.csv", index=False)

    # počty
    n_ok = {"malvér": int(((y == 1) & ok).sum()), "neškodné": int(((y == 0) & ok).sum()),
            "malvér spolu": int((y == 1).sum()), "neškodné spolu": int((y == 0).sum())}
    fam_ok = {f: f"{int(((fam == f) & ok).sum())} / {int((fam == f).sum())}" for f in FAMS}

    # kritérium R2 (docs/16)
    g = r2.set_index(["porovnanie", "súbory"])
    ceil = g.loc[("statický ALEBO dynamický − statický (horná hranica kombinácie)", "emulácia ok"), "_est"]
    hyb = g.loc[("hybrid − statický", "emulácia ok"), "_est"]
    spc = g.loc[("špecialista V3 − statický", "emulácia ok"), "_est"]
    r2_ok = ceil <= TOL and hyb <= TOL and spc <= TOL

    def md(df):
        df = df[[c for c in df.columns if not c.startswith("_")]]
        cols = list(df.columns)
        f = lambda v: f"{v:.4f}" if isinstance(v, float) and not np.isnan(v) else ("–" if isinstance(v, float) else str(v))
        return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] +
                         ["| " + " | ".join(f(v) for v in r) + " |" for r in df.itertuples(index=False)])

    rc_disp = rc.assign(**{"rozdiel [p. b.]": rc["rozdiel"].map(pp), "interval (2,5 – 97,5 %)": rc["2,5 %"].map(pp) + " až " + rc["97,5 %"].map(pp)})
    L = ["# Overenie robustnosti (docs/16)", "",
         "> Generované `src/evaluation/robustness.py`. Iba z uložených predikcií, prahy z validácie. Rozdiely v percentuálnych bodoch.",
         f"> R1: párový bootstrap testu ({B} opakovaní, stratifikovane), metrika = priemer cez seedy (v zero-day aj cez 7 rodín).",
         "> Pravidlá: *nižšie/horšie* = interval celý pod 0; *nie horšie* = dolná hranica > −1 p. b.; *rovnocenné* = interval v ±1 p. b.", "",
         "## R1 – štatistická významnosť", "", md(r1), "",
         "### Body 7 a 8 – zo scenára C (párovo cez 10 rozdelení × 3 seedy; interval = neistota výberu kalibračných súborov)", "",
         md(rc_disp[["tvrdenie", "test", "kalibrácia", "rozdiel [p. b.]", "interval (2,5 – 97,5 %)", "n párov"]]), "",
         "## R2 – iba súbory s úspešnou emuláciou", "",
         f"Testovacie súbory s úspešnou emuláciou: malvér {n_ok['malvér']} z {n_ok['malvér spolu']}, neškodné {n_ok['neškodné']} z {n_ok['neškodné spolu']}.",
         "Podľa rodiny (úspešné / všetky): " + ", ".join(f"{k} {v}" for k, v in fam_ok.items()) + ".", "",
         "### Úrovne (zero-day, priemer cez rodiny a seedy)", "", md(lev), "",
         "### Rozdiely oproti statickému modelu (zero-day, bootstrap)", "", md(r2), "",
         f"**Kritérium R2 (docs/16):** horná hranica kombinácie {pp(ceil)} p. b., hybrid {pp(hyb)} p. b., špecialista {pp(spc)} p. b. "
         f"na súboroch s úspešnou emuláciou → zistenie D **{'platí aj pri úspešnej emulácii' if r2_ok else 'treba zúžiť na emuláciu s chybami'}**.", ""]
    (out / "ROBUSTNESS.md").write_text("\n".join(L), encoding="utf-8")
    print(f"Robustnosť: {out / 'ROBUSTNESS.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", type=Path, default=Path("runs_final"))
    ap.add_argument("--v2", type=Path, default=Path("runs_v2"))
    ap.add_argument("--v3", type=Path, default=Path("runs_v3"))
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    main(a.v1, a.v2, a.v3, a.out or a.v3 / "comparison" / "robustness")
