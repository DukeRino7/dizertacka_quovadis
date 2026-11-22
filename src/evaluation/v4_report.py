r"""V4 (docs/19): súhrn KronoDroid – kritériá O1, O2 (s D-norm), tézy 1–4 a B1–B3, popisné porovnania.

Iba z uložených predikcií v runs_v4/<vetva>/{full,lofo/<rodina>,time}. Prahy rozhodnutí z validácie; hlavná miera
O1/O2 = TPR pri FPR 1 % odčítané z ROC krivky testu (metrika vyhodnotenia, nie ladenie). Intervaly: párový
stratifikovaný bootstrap testovacích súborov (B opakovaní; v zero-day v rámci každej rodiny), metrika = priemer cez
seedy (a v zero-day cez rodiny). real_p a emu_p majú rovnaké testovacie súbory -> rovnaké bootstrap váhy (párovo).

Zero-day: TPR vynechanej rodiny = všetky jej súbory (časť test + holdout = tréning a validácia, ktoré model nevidel),
FPR = neškodné súbory testu.

    .venv\Scripts\python.exe -m src.evaluation.v4_report --root runs_v4
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.cascade.components import Component
from src.cascade.evaluate_b import band, logit
from src.common.config import load_config
from src.common.paths import PROJECT_ROOT, rel
from src.common.provenance import git_info, now_iso, write_json

BRANCHES = ["real_full", "real_p", "emu_p"]
TOL = 0.01
LAB = {"static": "statický (vybraný)", "dynamic": "dynamický (vybraný)", "hybrid": "hybrid (vybraný)",
       "hybrid_mlp_large": "hybrid mlp_large (komplexný)", "kd_s": "statický študent mlp_kd",
       "kd_d": "dynamický študent mlp_kd", "kdh_s": "statický študent mlp_kd_heavy", "kdh_d": "dynamický študent mlp_kd_heavy",
       "A_main": "kaskáda A-main", "A_nokd": "kaskáda A-nokd", "A_modal": "kaskáda A-modal", "A_heavy": "kaskáda A-heavy",
       "A_baselines": "kaskáda A-baselines", "A_heavyteacher": "kaskáda A-heavyteacher",
       "B_main": "kaskáda B-main", "B_direct": "kaskáda B-direct", "B_heavy": "kaskáda B-heavy",
       "B_baselines": "kaskáda B-baselines", "B_nokd": "kaskáda B-nokd", "B_heavyteacher": "kaskáda B-heavyteacher",
       "B_baselines_10": "kaskáda B-baselines (rozpočet 10 %)", "spec": "špecialista V3 (B-spec, 10 %)",
       "spec_dyn": "špecialista V3 (B-spec-dyn, 10 %)", "S_or_D": "statický ALEBO dynamický (horná hranica)"}
CASCADES = [k for k in LAB if k.startswith(("A_", "B_")) or k.startswith("spec")]


# ----------------------------------------------------------------------------- načítanie jedného nastavenia

def chosen(root: Path, group: str) -> str:
    return json.loads((root / "selection" / f"{group}.json").read_text(encoding="utf-8"))["chosen"]


def _scores(c: Component, split: str, seed: int, sha: np.ndarray) -> np.ndarray:
    s = c.scores(split, seed).set_index("sha256")["score"].reindex(sha)
    if s.isna().any():
        raise ValueError(f"{rel(c.run)} {split}: chýbajú skóre pre {int(s.isna().sum())} súborov")
    return s.to_numpy()


class Setting:
    """Jedno nastavenie (vetva × hlavné / zero-day rodina / časový posun): skóre a rozhodnutia na teste (+ holdout)."""

    def __init__(self, root: Path, family: str | None = None):
        self.root, self.family = root, family
        sel = {g: chosen(root, g) for g in ("static", "dynamic", "hybrid")}
        self.selection = sel
        specs = {"static": sel["static"], "dynamic": sel["dynamic"], "hybrid": sel["hybrid"],
                 "hybrid_mlp_large": "hybrid/mlp_large",
                 "kd_s": "students_static/mlp_kd", "kd_d": "students_dynamic/mlp_kd",
                 "nokd_s": "students_static/mlp_nokd", "nokd_d": "students_dynamic/mlp_nokd",
                 "modal_s": "students_static/mlp_kd_modal", "modal_d": "students_dynamic/mlp_kd_modal",
                 "kdh_s": "students_static/mlp_kd_heavy", "kdh_d": "students_dynamic/mlp_kd_heavy"}
        if family is None and (root / "dynamic_ablations").exists():   # D-norm (iba hlavné rozdelenie)
            for g in ("dynamic", "hybrid"):
                arch = sel[g].split("/")[1]
                specs[f"{g}_norm"] = f"dynamic_ablations/{g[:3]}_{arch}_norm"
        self.comps = {k: Component(v, root) for k, v in specs.items() if self._exists(v)}
        missing = [k for k in specs if k not in self.comps and not k.endswith("_norm")]
        if missing:
            raise FileNotFoundError(f"{rel(root)}: nedokončené komponenty {missing}")
        self.seeds = sorted(set.intersection(*(set(c.seeds) for c in self.comps.values())))
        base = self.comps["static"].scores("test", self.seeds[0])
        self.meta = base[["sha256", "family", "label"]].reset_index(drop=True)
        self.has_holdout = family is not None and self.comps["static"].has_split("holdout", self.seeds[0])
        if self.has_holdout:
            self.hmeta = self.comps["static"].scores("holdout", self.seeds[0])[["sha256", "family", "label"]].reset_index(drop=True)
        self.spec = {v: self._latest(root / "cascade" / f"v4_{v.replace('-', '_')}") for v in ("spec", "spec_dyn")}

    def _exists(self, spec: str) -> bool:
        base = self.root / spec
        return base.exists() and any((r / "metrics.json").exists() for r in base.iterdir() if r.is_dir())

    @staticmethod
    def _latest(base: Path):
        runs = sorted(r for r in base.iterdir() if (r / "metrics.json").exists()) if base.exists() else []
        return runs[-1] if runs else None

    def seed_data(self, seed: int) -> dict:
        """Skóre, prahy a rozhodnutia všetkých prístupov pre jeden seed (test a prípadne holdout)."""
        parts = {"test": self.meta["sha256"].to_numpy()}
        if self.has_holdout:
            parts["holdout"] = self.hmeta["sha256"].to_numpy()
        V = self.meta  # placeholder pre čitateľnosť
        sha_v = self.comps["static"].scores("validation", seed)["sha256"].to_numpy()
        yv = self.comps["static"].scores("validation", seed).set_index("sha256").loc[sha_v, "label"].to_numpy()
        thr = {k: c.threshold(seed) for k, c in self.comps.items()}
        S = {p: {k: _scores(c, p, seed, sha) for k, c in self.comps.items()} for p, sha in parts.items()}
        sv = _scores(self.comps["static"], "validation", seed, sha_v)
        svs = {k: _scores(self.comps[k], "validation", seed, sha_v) for k in ("static", "kd_s", "nokd_s", "kdh_s")}
        out = {"scores": {p: S[p] for p in parts}, "dec": {}}
        for p in parts:
            dec = {k: S[p][k] >= thr[k] for k in self.comps}
            d = {k: dec[k] for k in ("static", "dynamic", "hybrid", "hybrid_mlp_large", "kd_s", "kd_d", "kdh_s", "kdh_d")}
            for k in ("dynamic_norm", "hybrid_norm"):
                if k in dec:
                    d[k] = dec[k]

            rates, hyb_rates = {}, {}

            def casc_a(s, dd, h, name):
                d[name] = np.where(dec[s] == dec[dd], dec[s], dec[h])
                hyb_rates[name] = float((dec[s] != dec[dd]).mean())   # podiel eskalácií na hybrid
            casc_a("kd_s", "kd_d", "hybrid", "A_main")
            casc_a("nokd_s", "nokd_d", "hybrid", "A_nokd")
            casc_a("modal_s", "modal_d", "hybrid", "A_modal")
            casc_a("kd_s", "kd_d", "hybrid_mlp_large", "A_heavy")
            casc_a("static", "dynamic", "hybrid", "A_baselines")
            casc_a("kdh_s", "kdh_d", "hybrid", "A_heavyteacher")

            def casc_b(first, second, hyb, name, budget=None):
                s = S[p][first]
                if budget is None:
                    lo, hi = band(svs[first], yv, 0.001, 0.01)
                    unc = (s >= lo) & (s < hi)
                    sure = s >= hi
                else:
                    dv = np.abs(logit(svs[first]) - logit(thr[first]))
                    unc = np.abs(logit(s) - logit(thr[first])) <= np.quantile(dv, budget)
                    sure = dec[first]
                if second is None:
                    fin = np.where(unc, dec[hyb], sure)
                    hyb_rates[name] = float(unc.mean())
                else:
                    fin = np.where(unc, np.where(dec[second] != dec[first], dec[hyb], dec[first]), sure)
                    hyb_rates[name] = float((unc & (dec[second] != dec[first])).mean())
                d[name] = fin.astype(bool)
                rates[name] = float(unc.mean())
            casc_b("kd_s", "kd_d", "hybrid", "B_main")
            casc_b("kd_s", None, "hybrid", "B_direct")
            casc_b("kd_s", "kd_d", "hybrid_mlp_large", "B_heavy")
            casc_b("static", "dynamic", "hybrid", "B_baselines")
            casc_b("nokd_s", "nokd_d", "hybrid", "B_nokd")
            casc_b("kdh_s", "kdh_d", "hybrid", "B_heavyteacher")
            casc_b("static", "dynamic", "hybrid", "B_baselines_10", budget=0.1)
            for v, run in self.spec.items():
                if run is None:
                    continue
                m = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
                ps = next((r for r in m["per_seed"] if r["seed"] == seed), None)
                f = run / "predictions" / f"{p}_seed{seed}.parquet"
                if ps is None or not f.exists():
                    continue
                P = pd.read_parquet(f).set_index("sha256").reindex(parts[p])
                t_sp = ps["budgets"][str(m["config"]["main_budget"])]["spec_threshold"]
                esc = P["escalated_main"].to_numpy(bool)
                d[v] = np.where(esc, P["score"].to_numpy() >= t_sp, P["s_static"].to_numpy() >= ps["thresholds"]["static"])
                rates[v] = float(esc.mean())
            d["S_or_D"] = dec["static"] | dec["dynamic"]
            out["dec"][p] = {k: np.asarray(v, bool) for k, v in d.items()}
            out[f"rates_{p}"] = rates
            out[f"hyb_rates_{p}"] = hyb_rates
        return out


# ----------------------------------------------------------------------------- bootstrap

def boot_counts(n_idx: int, B: int, rng) -> np.ndarray:
    return np.stack([np.bincount(rng.integers(0, n_idx, n_idx), minlength=n_idx) for _ in range(B)]).astype(np.float32)


def tpr_at_fpr_w(s_ben, s_mal, wb, wm, fpr=0.01):
    """TPR pri FPR ≤ fpr z ROC (vážené; wb, wm = B×n váhy alebo 1×n jednotky). Vracia vektor dĺžky B."""
    o = np.argsort(-s_ben, kind="stable")
    sb, wbs = s_ben[o], wb[:, o]
    cum = np.cumsum(wbs, axis=1) / wbs.sum(axis=1, keepdims=True)
    k = (cum <= fpr + 1e-12).sum(axis=1)                       # počet neškodných, ktoré smú byť nad prahom
    thr = np.where(k < len(sb), sb[np.minimum(k, len(sb) - 1)], -np.inf)
    hit = s_mal[None, :] > thr[:, None]
    return (wm * hit).sum(axis=1) / wm.sum(axis=1)


def rate_w(d, w):
    return (w @ d.astype(np.float32)) / w.sum(axis=1)


class Boot:
    """Spoločné bootstrap váhy pre jedno rozdelenie testu (benign, malvér; v zero-day malvér rodiny)."""

    def __init__(self, y: np.ndarray, B: int, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.ben, self.mal = np.flatnonzero(y == 0), np.flatnonzero(y == 1)
        self.Wb, self.Wm = boot_counts(len(self.ben), B, rng), boot_counts(len(self.mal), B, rng)
        self.one_b, self.one_m = np.ones((1, len(self.ben)), np.float32), np.ones((1, len(self.mal)), np.float32)


def ci(v: np.ndarray, point: float) -> dict:
    return {"point": float(point), "lo": float(np.percentile(v, 2.5)), "hi": float(np.percentile(v, 97.5))}


# ----------------------------------------------------------------------------- metriky cez seedy

def main_metrics(st: Setting, data: list[dict], boot: Boot) -> dict:
    """Hlavné rozdelenie: TPR pri FPR 1 % (ROC testu) pre skóre a TPR/FPR pri prahoch z validácie pre rozhodnutia."""
    y = st.meta["label"].to_numpy()
    res = {"roc": {}, "dec": {}, "auc": {}}
    for k in ("static", "dynamic", "hybrid", "hybrid_mlp_large", "dynamic_norm", "hybrid_norm", "kd_s", "kd_d", "kdh_s", "kdh_d"):
        if k not in data[0]["scores"]["test"]:
            continue
        pts, bs, aucs = [], [], []
        for D in data:
            s = D["scores"]["test"][k]
            pts.append(tpr_at_fpr_w(s[boot.ben], s[boot.mal], boot.one_b, boot.one_m)[0])
            bs.append(tpr_at_fpr_w(s[boot.ben], s[boot.mal], boot.Wb, boot.Wm))
            aucs.append(roc_auc_score(y, s))
        res["roc"][k] = (float(np.mean(pts)), np.mean(bs, axis=0))
        res["auc"][k] = float(np.mean(aucs))
    for k in data[0]["dec"]["test"]:
        tp = [D["dec"]["test"][k][boot.mal].mean() for D in data]
        fp = [D["dec"]["test"][k][boot.ben].mean() for D in data]
        btp = np.mean([rate_w(D["dec"]["test"][k][boot.mal], boot.Wm) for D in data], axis=0)
        bfp = np.mean([rate_w(D["dec"]["test"][k][boot.ben], boot.Wb) for D in data], axis=0)
        res["dec"][k] = {"tpr": (float(np.mean(tp)), btp), "fpr": (float(np.mean(fp)), bfp)}
    res["rates"] = {k: float(np.mean([D["rates_test"].get(k, np.nan) for D in data])) for k in data[0]["rates_test"]}
    res["hyb_rates"] = {k: float(np.mean([D["hyb_rates_test"].get(k, np.nan) for D in data])) for k in data[0]["hyb_rates_test"]}
    return res


def zero_day_metrics(settings: list[Setting], datas: list[list[dict]], B: int) -> dict:
    """Zero-day: priemer cez rodiny; TPR rodiny = test + holdout; FPR = neškodné testu. Bootstrap v rámci rodiny."""
    per_fam = {}
    roc_keys = ("static", "dynamic", "hybrid", "hybrid_mlp_large", "kd_s", "kd_d", "kdh_s", "kdh_d")
    for st, data in zip(settings, datas):
        y, fam = st.meta["label"].to_numpy(), st.meta["family"].to_numpy()
        ben = np.flatnonzero(y == 0)
        mal_t = np.flatnonzero((y == 1) & (fam == st.family))
        nh = len(st.hmeta) if st.has_holdout else 0
        rng = np.random.default_rng(1)
        Wb = boot_counts(len(ben), B, rng)
        Wm = boot_counts(len(mal_t) + nh, B, rng)
        ob, om = np.ones((1, len(ben)), np.float32), np.ones((1, len(mal_t) + nh), np.float32)

        def fam_vec(D, kind, k):
            v = D[kind]["test"][k][mal_t]
            return np.concatenate([v, D[kind]["holdout"][k]]) if nh else v
        r = {"roc": {}, "dec": {}, "n_family": int(len(mal_t) + nh)}
        for k in roc_keys:
            if k not in data[0]["scores"]["test"]:
                continue
            pts = [tpr_at_fpr_w(D["scores"]["test"][k][ben], fam_vec(D, "scores", k), ob, om)[0] for D in data]
            bs = [tpr_at_fpr_w(D["scores"]["test"][k][ben], fam_vec(D, "scores", k), Wb, Wm) for D in data]
            r["roc"][k] = (float(np.mean(pts)), np.mean(bs, axis=0))
        for k in data[0]["dec"]["test"]:
            if any(k not in D["dec"].get("holdout", D["dec"]["test"]) for D in data):
                continue
            tp = [fam_vec(D, "dec", k).mean() for D in data]
            fp = [D["dec"]["test"][k][ben].mean() for D in data]
            btp = np.mean([rate_w(fam_vec(D, "dec", k), Wm) for D in data], axis=0)
            bfp = np.mean([rate_w(D["dec"]["test"][k][ben], Wb) for D in data], axis=0)
            r["dec"][k] = {"tpr": (float(np.mean(tp)), btp), "fpr": (float(np.mean(fp)), bfp)}
        r["rates"] = {k: float(np.mean([D["rates_test"].get(k, np.nan) for D in data])) for k in data[0]["rates_test"]}
        per_fam[st.family] = r
    # priemer cez rodiny (bodovo aj v každom bootstrap opakovaní)
    fams = list(per_fam)
    avg = {"roc": {}, "dec": {}, "rates": {}}
    for k in per_fam[fams[0]]["roc"]:
        avg["roc"][k] = (float(np.mean([per_fam[f]["roc"][k][0] for f in fams])), np.mean([per_fam[f]["roc"][k][1] for f in fams], axis=0))
    for k in per_fam[fams[0]]["dec"]:
        if all(k in per_fam[f]["dec"] for f in fams):
            avg["dec"][k] = {m: (float(np.mean([per_fam[f]["dec"][k][m][0] for f in fams])),
                                 np.mean([per_fam[f]["dec"][k][m][1] for f in fams], axis=0)) for m in ("tpr", "fpr")}
    for k in per_fam[fams[0]]["rates"]:
        avg["rates"][k] = float(np.mean([per_fam[f]["rates"].get(k, np.nan) for f in fams]))
    return {"per_family": per_fam, "avg": avg, "families": fams}


def diff(a, b) -> dict:
    return ci(a[1] - b[1], a[0] - b[0])


# ----------------------------------------------------------------------------- hlavný postup

def load_branch(root: Path, branch: str, families: list[str], B: int, boot_main: Boot | None):
    base = root / branch
    st = Setting(base / "full")
    data = [st.seed_data(s) for s in st.seeds]
    boot = boot_main or Boot(st.meta["label"].to_numpy(), B)
    M = main_metrics(st, data, boot)
    Z = None
    lofo = [(f, base / "lofo" / f.replace("/", "_").replace(" ", "_")) for f in families]
    lofo = [(f, p) for f, p in lofo if (p / "selection").exists()]
    if lofo:
        sts = [Setting(p, f) for f, p in lofo]
        Z = zero_day_metrics(sts, [[s.seed_data(x) for x in s.seeds] for s in sts], B)
    T = None
    if branch == "real_full" and (base / "time" / "selection").exists():
        stt = Setting(base / "time")
        T = main_metrics(stt, [stt.seed_data(s) for s in stt.seeds], Boot(stt.meta["label"].to_numpy(), B))
    return {"setting": st, "boot": boot, "main": M, "zero": Z, "time": T}


def cost(root: Path, spec: str) -> float | None:
    try:
        c = Component(spec, root).cost()
        return c["cpu_ms_batch"] if c else None
    except FileNotFoundError:
        return None


def pp(x: float) -> str:
    return f"{100 * x:+.2f}"


def fmt_ci(c: dict) -> str:
    return f"{pp(c['point'])} ({pp(c['lo'])} až {pp(c['hi'])})"


def verdict_gain(c: dict) -> bool:
    return c["point"] >= TOL and c["lo"] > 0


def thesis_rows(M: dict, Z: dict | None) -> list[dict]:
    rows = []
    for k in CASCADES:
        if k not in M["dec"]:
            continue
        s, d, c = M["dec"]["static"], M["dec"]["dynamic"], M["dec"][k]
        t2 = (c["fpr"][0] < s["fpr"][0]) and (c["fpr"][0] < d["fpr"][0]) and (c["tpr"][0] >= s["tpr"][0] - TOL)
        row = {"kaskáda": LAB[k], "TPR": c["tpr"][0], "FPR": c["fpr"][0], "téza 2 (hlavné)": t2,
               "dyn. analýza": M["rates"].get(k)}
        if Z and k in Z["avg"]["dec"]:
            zs, zd, zc = Z["avg"]["dec"]["static"], Z["avg"]["dec"]["dynamic"], Z["avg"]["dec"][k]
            row["TPR rodiny (zero-day)"] = zc["tpr"][0]
            row["téza 1"] = (zc["tpr"][0] >= zs["tpr"][0] + TOL) and (zc["fpr"][0] <= zs["fpr"][0])
            row["téza 2 (zero-day)"] = (zc["fpr"][0] < zs["fpr"][0]) and (zc["fpr"][0] < zd["fpr"][0]) and (zc["tpr"][0] >= zs["tpr"][0] - TOL)
        rows.append(row)
    return rows


def md(df: pd.DataFrame) -> str:
    def f(v):
        if isinstance(v, (bool, np.bool_)):
            return "**áno**" if v else "nie"
        if isinstance(v, float):
            return "–" if np.isnan(v) else f"{v:.4f}"
        return str(v)
    head = "| " + " | ".join(df.columns) + " |\n|" + "---|" * len(df.columns) + "\n"
    return head + "\n".join("| " + " | ".join(f(v) for v in r) + " |" for r in df.itertuples(index=False))


def main(root: Path, B: int) -> None:
    cfg = load_config("configs/kronodroid/data.yaml")
    families = cfg["v4"]["holdout_families"]
    out = root / "comparison" / "v4"
    out.mkdir(parents=True, exist_ok=True)
    R = {}
    for b in BRANCHES:
        if not (root / b / "full" / "selection").exists():
            print(f"{b}: chýba, preskakujem", flush=True)
            continue
        boot = R["real_p"]["boot"] if b == "emu_p" and "real_p" in R else None   # párovo: rovnaké testovacie súbory
        if boot is not None:
            assert (R["real_p"]["setting"].meta["sha256"].to_numpy() == Setting(root / b / "full").meta["sha256"].to_numpy()).all()
        try:
            R[b] = load_branch(root, b, families, B, boot)
        except FileNotFoundError as e:
            print(f"{b}: preskakujem – {e}", flush=True)
            continue
        print(f"{b}: načítané", flush=True)

    summary, lines = {"created": now_iso(), "root": rel(root), "B": B, "git": git_info()}, []
    # --- O1 (real_full) a O2 (real_p − emu_p) ---------------------------------------------------------------------
    crit = []

    def gain(M, num="hybrid", kind="roc"):
        return diff(M[kind][num], M[kind]["static"])
    if "real_full" in R:
        M, Z = R["real_full"]["main"], R["real_full"]["zero"]
        o1 = gain(M)
        crit.append(("O1", "real_full, hlavné: hybrid − statický (TPR pri FPR 1 %)", o1, verdict_gain(o1)))
        if Z:
            o1z = diff(Z["avg"]["roc"]["hybrid"], Z["avg"]["roc"]["static"])
            crit.append(("O1-Z", "real_full, zero-day (priemer rodín): hybrid − statický", o1z, verdict_gain(o1z)))
        if "hybrid_norm" in M["roc"]:
            dn = diff(M["roc"]["hybrid_norm"], M["roc"]["static"])
            crit.append(("D-norm (real_full)", "hybrid s podielmi volaní − statický", dn, dn["point"] >= TOL))
    if "real_p" in R and "emu_p" in R:
        Mr, Me = R["real_p"]["main"], R["emu_p"]["main"]
        dr = (Mr["roc"]["hybrid"][0] - Mr["roc"]["static"][0], Mr["roc"]["hybrid"][1] - Mr["roc"]["static"][1])
        de = (Me["roc"]["hybrid"][0] - Me["roc"]["static"][0], Me["roc"]["hybrid"][1] - Me["roc"]["static"][1])
        crit.append(("Δ real_p", "real_p: hybrid − statický", diff(Mr["roc"]["hybrid"], Mr["roc"]["static"]), None))
        crit.append(("Δ emu_p", "emu_p: hybrid − statický", diff(Me["roc"]["hybrid"], Me["roc"]["static"]), None))
        o2 = ci(dr[1] - de[1], dr[0] - de[0])
        crit.append(("O2", "Δ real_p − Δ emu_p", o2, verdict_gain(o2)))
        Zr, Ze = R["real_p"]["zero"], R["emu_p"]["zero"]
        if Zr and Ze:
            zr = (Zr["avg"]["roc"]["hybrid"][0] - Zr["avg"]["roc"]["static"][0], Zr["avg"]["roc"]["hybrid"][1] - Zr["avg"]["roc"]["static"][1])
            ze = (Ze["avg"]["roc"]["hybrid"][0] - Ze["avg"]["roc"]["static"][0], Ze["avg"]["roc"]["hybrid"][1] - Ze["avg"]["roc"]["static"][1])
            o2z = ci(zr[1] - ze[1], zr[0] - ze[0])
            crit.append(("O2-Z", "zero-day: Δ real_p − Δ emu_p", o2z, verdict_gain(o2z)))
            # párovo: rovnaké súbory v rovnakom poradí (statické predikcie sú zdieľané) a rovnaký seed váh v každej rodine
            for f in Zr["families"]:
                assert Zr["per_family"][f]["n_family"] == Ze["per_family"][f]["n_family"]
        for b in ("real_p", "emu_p"):
            M = R[b]["main"]
            if "hybrid_norm" in M["roc"]:
                dn = diff(M["roc"]["hybrid_norm"], M["roc"]["static"])
                crit.append((f"D-norm ({b})", "hybrid s podielmi volaní − statický", dn, dn["point"] >= TOL))
    summary["criteria"] = [{"id": i, "what": w, **c, "met": m} for i, w, c, m in crit]
    lines.append("## 1. Hlavné otázky (docs/19, oddiel 4)\nRozdiel v p. b., 95 % interval z párového bootstrapu "
                 f"({B} opakovaní). Kritérium O1/O2: rozdiel ≥ +1 p. b. a dolná hranica > 0.\n")
    lines.append("| | čo | rozdiel (IS) | splnené |\n|---|---|---|---|\n" + "\n".join(
        f"| {i} | {w} | {fmt_ci(c)} | {'–' if m is None else ('**áno**' if m else 'nie')} |" for i, w, c, m in crit))
    met = {i: m for i, _, _, m in crit}
    if "O1" in met and "O2" in met:
        if met["O1"] and met["O2"]:
            concl = "O1 aj O2 platia → **podporuje** vysvetlenie, že slabinou Quo Vadis bola emulácia."
        elif met["O1"]:
            concl = "O1 platí, O2 nie → dynamika pomáha aj z emulátora; rozdiel oproti Quo Vadis je skôr vo vlastnostiach datasetu."
        else:
            concl = "O1 neplatí → ani kvalitnejšia dynamika nepridáva informáciu nad statiku; **oslabuje** vysvetlenie „slabinou bola emulácia“."
        lines.append(f"\n**Interpretácia podľa docs/19, 4.3:** {concl}")
        dn = [c for i, _, c, _ in crit if i == "D-norm (real_full)"]
        if met["O1"] and dn and dn[0]["point"] < TOL:
            lines.append("\n**D-norm:** prínos s podielmi volaní zmizne → stojí na celkovom množstve aktivity (možný artefakt zberu).")

    # --- O1/O2 pre kaskády: rozdiel TPR a FPR oproti statickému modelu (prahy z validácie), všetky varianty ----------
    cr = []
    for b, X in R.items():
        M = X["main"]
        for k in CASCADES:
            if k in M["dec"]:
                cr.append({"vetva": b, "kaskáda": LAB[k], "ΔTPR vs. statický": fmt_ci(diff(M["dec"][k]["tpr"], M["dec"]["static"]["tpr"])),
                           "ΔFPR vs. statický": fmt_ci(diff(M["dec"][k]["fpr"], M["dec"]["static"]["fpr"]))})
    if cr:
        lines.append("\n### Kaskády oproti statickému modelu (prahy z validácie; p. b., 95 % IS)\nVšetky varianty, bez výberu "
                     "podľa testu.\n\n" + md(pd.DataFrame(cr)))
        summary["cascades_vs_static"] = cr

    # --- popisné: modely podľa vetvy ---------------------------------------------------------------------------------
    rows = []
    for b, X in R.items():
        M = X["main"]
        for k in ("static", "dynamic", "hybrid", "hybrid_mlp_large", "dynamic_norm", "hybrid_norm"):
            if k in M["roc"]:
                rows.append({"vetva": b, "model": LAB.get(k, k), "ROC-AUC": M["auc"][k], "TPR pri FPR 1 % (test)": M["roc"][k][0],
                             "TPR (prah z val.)": M["dec"][k]["tpr"][0] if k in M["dec"] else np.nan,
                             "FPR (prah z val.)": M["dec"][k]["fpr"][0] if k in M["dec"] else np.nan})
        rows.append({"vetva": b, "model": LAB["S_or_D"], "ROC-AUC": np.nan, "TPR pri FPR 1 % (test)": np.nan,
                     "TPR (prah z val.)": M["dec"]["S_or_D"]["tpr"][0], "FPR (prah z val.)": M["dec"]["S_or_D"]["fpr"][0]})
    sel = {b: X["setting"].selection for b, X in R.items()}
    lines.append("\n## 2. Modely na hlavnom rozdelení (priemer cez seedy)\nVybrané modely: " +
                 "; ".join(f"{b}: " + ", ".join(f"{g}={v}" for g, v in s.items()) for b, s in sel.items()) + "\n\n" + md(pd.DataFrame(rows)))
    summary["models"] = rows
    summary["selection"] = sel

    # --- zero-day po rodinách ---------------------------------------------------------------------------------------
    zr = []
    for b, X in R.items():
        if not X["zero"]:
            continue
        for f, r in X["zero"]["per_family"].items():
            zr.append({"vetva": b, "rodina": f, "n": r["n_family"], **{LAB[k]: r["roc"][k][0] for k in ("static", "dynamic", "hybrid") if k in r["roc"]}})
        a = X["zero"]["avg"]["roc"]
        zr.append({"vetva": b, "rodina": "**priemer**", "n": "", **{LAB[k]: a[k][0] for k in ("static", "dynamic", "hybrid") if k in a}})
    if zr:
        lines.append("\n## 3. Zero-day: TPR vynechanej rodiny pri FPR 1 % (ROC testu; rodina = test + holdout)\n" + md(pd.DataFrame(zr)))
        summary["zero_day"] = zr

    # --- tézy -------------------------------------------------------------------------------------------------------
    for b, X in R.items():
        T = pd.DataFrame(thesis_rows(X["main"], X["zero"]))
        lines.append(f"\n## 4. Tézy 1, 2, 4 – vetva {b} (prahy z validácie, kritériá docs/09)\n"
                     "Referencie: statický TPR/FPR "
                     f"{X['main']['dec']['static']['tpr'][0]:.4f} / {X['main']['dec']['static']['fpr'][0]:.4f}, dynamický "
                     f"{X['main']['dec']['dynamic']['tpr'][0]:.4f} / {X['main']['dec']['dynamic']['fpr'][0]:.4f}. "
                     "„dyn. analýza“ = podiel testovacích súborov s dynamickou analýzou (kaskády A = 100 %).\n\n" + md(T))
        summary[f"theses_{b}"] = T.to_dict("records")

    # --- téza 3: študenti vs. komplexný hybrid ---------------------------------------------------------------------
    t3 = []
    for b, X in R.items():
        root_b = root / b / "full"
        c_h = cost(root_b, "hybrid/mlp_large")
        for k, spec in [("kd_s", "students_static/mlp_kd"), ("kd_d", "students_dynamic/mlp_kd"),
                        ("kdh_s", "students_static/mlp_kd_heavy"), ("kdh_d", "students_dynamic/mlp_kd_heavy")]:
            if k not in X["main"]["dec"]:
                continue
            dtp = X["main"]["dec"][k]["tpr"][0] - X["main"]["dec"]["hybrid_mlp_large"]["tpr"][0]
            ztp = (X["zero"]["avg"]["dec"][k]["tpr"][0] - X["zero"]["avg"]["dec"]["hybrid_mlp_large"]["tpr"][0]) if X["zero"] else np.nan
            c_s = cost(root_b, spec)
            t3.append({"vetva": b, "študent": LAB[k], "ΔTPR vs. mlp_large hybrid (hlavné)": dtp, "ΔTPR rodiny (zero-day)": ztp,
                       "CPU ms/vz. študent": c_s if c_s is not None else np.nan, "CPU ms/vz. mlp_large": c_h if c_h is not None else np.nan,
                       "téza 3": (abs(dtp) <= TOL or dtp > 0) and (np.isnan(ztp) or ztp >= -TOL) and (c_s is not None and c_h is not None and c_s < c_h)})
    if t3:
        lines.append("\n## 5. Téza 3 – študent vs. komplexný hybrid (mlp_large)\nKritérium: TPR nie horšie o viac ako 1 p. b. "
                     "(hlavné aj zero-day) pri nižšom CPU čase na vzorku.\n\n" + md(pd.DataFrame(t3)))
        summary["thesis3"] = t3

    # --- B1–B3 (špecialista V3) -------------------------------------------------------------------------------------
    bb = []
    for b, X in R.items():
        Z = X["zero"]
        if not Z or "spec" not in Z["avg"]["dec"]:
            continue
        zs, zsp, zb = Z["avg"]["dec"]["static"], Z["avg"]["dec"]["spec"], Z["avg"]["dec"]["B_baselines_10"]
        wins = sum(Z["per_family"][f]["dec"]["spec"]["tpr"][0] >= Z["per_family"][f]["dec"]["static"]["tpr"][0] for f in Z["families"])
        M = X["main"]["dec"]
        b2 = M["spec"]["fpr"][0] < M["static"]["fpr"][0] and M["spec"]["fpr"][0] < M["dynamic"]["fpr"][0] and M["spec"]["tpr"][0] >= M["static"]["tpr"][0] - TOL
        bb.append({"vetva": b, "TPR rodiny špecialista": zsp["tpr"][0], "TPR rodiny statický": zs["tpr"][0],
                   "rodiny spec ≥ stat": f"{wins} z {len(Z['families'])}",
                   "B1": zsp["tpr"][0] >= zs["tpr"][0] + TOL and zsp["fpr"][0] <= zs["fpr"][0] and wins >= 4,
                   "B2 (hlavné)": b2,
                   "B3": zsp["tpr"][0] >= zb["tpr"][0] + TOL and zsp["fpr"][0] <= zb["fpr"][0] + 0.001})
    if bb:
        lines.append("\n## 6. Špecialista V3 – kritériá B1–B3 (docs/19, 3.4)\n" + md(pd.DataFrame(bb)))
        summary["B1_B3"] = bb

    # --- výpočtové nároky (benchmark z hlavného rozdelenia, docs/03) ---------------------------------------------
    for b_, X in R.items():
        root_b = root / b_ / "full"
        sel_b = X["setting"].selection
        models = [("statický", sel_b["static"]), ("dynamický", sel_b["dynamic"]), ("hybrid", sel_b["hybrid"]),
                  ("hybrid komplexný", "hybrid/mlp_large"), ("statický študent mlp_kd", "students_static/mlp_kd"),
                  ("dynamický študent mlp_kd", "students_dynamic/mlp_kd"), ("statický študent mlp_kd_heavy", "students_static/mlp_kd_heavy"),
                  ("dynamický študent mlp_kd_heavy", "students_dynamic/mlp_kd_heavy")]
        rows, cpu = [], {}
        for lab_, spec in models:
            try:
                c = Component(spec, root_b)
            except FileNotFoundError:
                continue
            tm = json.loads((c.run / "timing.json").read_text(encoding="utf-8")) if (c.run / "timing.json").exists() else {}
            bm = c.benchmark or {}
            cb, cs = bm.get("cpu_batch", {}), bm.get("cpu_single", {})
            cpu[spec] = cb.get("cpu_ms_per_sample")
            rows.append({"model": f"{lab_} ({spec})", "CPU ms/vz. dávka": cb.get("cpu_ms_per_sample", np.nan),
                         "CPU ms/vz. 1 vz.": cs.get("cpu_ms_per_sample", np.nan), "latencia ms (medián)": cs.get("latency_median_ms", np.nan),
                         "GPU J/1000 vz.": (bm.get("gpu_batch") or {}).get("gpu_energy_above_idle_j_per_1000", np.nan),
                         "parametre/uzly": tm.get("n_parameters", np.nan), "disk MB": tm.get("model_disk_bytes", np.nan) / 1e6 if tm else np.nan,
                         "tréning s (seed)": float(np.mean(tm["fit_s_per_seed"])) if tm.get("fit_s_per_seed") else np.nan,
                         "ladenie s": tm.get("hpo_s", np.nan)})
        lines.append(f"\n## 8. Výpočtové nároky – vetva {b_} (benchmark, model zo seedu 0; čas dynamickej analýzy dataset neuvádza)\n"
                     + md(pd.DataFrame(rows)))
        # odhad kaskád: A = statický + dynamický + eskalácie × hybrid; B = statický + podiel dyn. analýzy × dynamický + podiel na hybrid × hybrid
        comp_of = {"A_main": ("students_static/mlp_kd", "students_dynamic/mlp_kd", sel_b["hybrid"]),
                   "A_baselines": (sel_b["static"], sel_b["dynamic"], sel_b["hybrid"]),
                   "A_heavy": ("students_static/mlp_kd", "students_dynamic/mlp_kd", "hybrid/mlp_large"),
                   "B_main": ("students_static/mlp_kd", "students_dynamic/mlp_kd", sel_b["hybrid"]),
                   "B_baselines": (sel_b["static"], sel_b["dynamic"], sel_b["hybrid"]),
                   "B_baselines_10": (sel_b["static"], sel_b["dynamic"], sel_b["hybrid"]),
                   "B_heavy": ("students_static/mlp_kd", "students_dynamic/mlp_kd", "hybrid/mlp_large")}
        cr2 = []
        M = X["main"]
        for k, (s_, d_, h_) in comp_of.items():
            if k not in M["hyb_rates"] or None in (cpu.get(s_), cpu.get(d_), cpu.get(h_)):
                continue
            dyn_share = 1.0 if k.startswith("A_") else M["rates"][k]
            est = cpu[s_] + dyn_share * cpu[d_] + M["hyb_rates"][k] * cpu[h_]
            cr2.append({"kaskáda": LAB[k], "podiel dyn. analýzy": dyn_share, "podiel na hybrid": M["hyb_rates"][k],
                        "CPU ms/vz. (odhad)": est, "hybrid na každej vzorke": cpu[h_], "statický samostatne": cpu[sel_b["static"]]})
        if cr2:
            lines.append("\nOdhad CPU času kaskád (dávka) zo súčtu komponentov a podielov na teste:\n\n" + md(pd.DataFrame(cr2)))
        summary[f"costs_{b_}"] = {"models": rows, "cascades": cr2}

    # --- časový posun malvéru -----------------------------------------------------------------------------------------
    if "real_full" in R and R["real_full"]["time"]:
        Tm = R["real_full"]["time"]
        rows = [{"model": LAB[k], "TPR pri FPR 1 % (test)": Tm["roc"][k][0], "ROC-AUC": Tm["auc"][k]} for k in ("static", "dynamic", "hybrid") if k in Tm["roc"]]
        lines.append("\n## 7. Doplnkovo: časový posun malvéru (real_time, test = malvér 2015–2020)\n" + md(pd.DataFrame(rows)) +
                     f"\n\nhybrid − statický: {fmt_ci(diff(Tm['roc']['hybrid'], Tm['roc']['static']))}")
        summary["time"] = rows

    text = (f"# Súhrn V4 – KronoDroid\n\n> Generované `src/evaluation/v4_report.py` ({now_iso()}) z `{rel(root)}`. "
            "Plán a kritériá: `docs/19_plan_v4.md`. Hlavná miera O1/O2: TPR pri FPR 1 % z ROC krivky testu.\n\n" + "\n".join(lines) + "\n")
    (out / "README.md").write_text(text, encoding="utf-8")
    write_json(summary, out / "summary.json")
    print(f"Súhrn V4: {rel(out / 'README.md')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="runs_v4")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    main(PROJECT_ROOT / a.root, a.boot)
