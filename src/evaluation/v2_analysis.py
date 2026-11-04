r"""Analýza príčin výsledkov V2 (zero-day): prečo kaskáda neprekoná statický model a kde je priestor na zlepšenie.

Iba z uložených predikcií `runs_v2/lofo/<rodina>/{static,dynamic,hybrid}/lightgbm`, prahy z validácie (FPR 1 %),
priemer cez seedy 0–2. Nič sa nenastavuje podľa testu. Diagnostické veličiny, ktoré test používajú
(prah pri FPR na teste, „dokonalý“ druhý stupeň), sú **horné hranice / orákulá** – slúžia iba na vysvetlenie, nikdy
nie ako výsledok metódy.

    .venv\Scripts\python.exe -m src.evaluation.v2_analysis --root runs_v2
"""
import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.evaluation.metrics import threshold_for_fpr

FAMS = ["backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan"]
APPS = {"S": "static/lightgbm", "D": "dynamic/lightgbm", "H": "hybrid/lightgbm"}
BUDGET = 0.10   # rozpočet emulácie (docs/09): podiel validácie najbližšie prahu statického modelu
TINY = 5        # malý report = najviac 5 API volaní (configs/data/dynamic.yaml, audit)


def logit(p):
    p = np.clip(p, 1e-7, 1 - 1e-7)
    return np.log(p / (1 - p))


def load(root: Path, fam: str, app: str, split: str, seed: int) -> pd.DataFrame:
    f = sorted(glob.glob(str(root / "lofo" / fam / app / "*" / "predictions" / f"{split}_seed{seed}.parquet")))[-1]
    return pd.read_parquet(f)


def emulation_subsets() -> pd.Series:
    parts = [pd.read_parquet(f"processed/dynamic/cache/{s}.parquet", columns=["sha256", "n_api_calls", "module_entry_error"])
             for s in ("train", "validation", "test")]
    e = pd.concat(parts).drop_duplicates("sha256").set_index("sha256")
    return pd.Series(np.where(e["n_api_calls"] <= TINY, "malý report",
                              np.where(e["module_entry_error"] == "unsupported_api", "unsupported_api", "emulácia ok")), index=e.index)


def analyze(root: Path):
    emu = emulation_subsets()
    rows, subs = [], []
    for fam in FAMS:
        for seed in range(3):
            P = {k: {s: load(root, fam, a, s, seed) for s in ("validation", "test", "holdout")} for k, a in APPS.items()}
            thr = {k: threshold_for_fpr(P[k]["validation"].label.values, P[k]["validation"].score.values, 0.01) for k in P}
            t = P["S"]["test"]
            assert all((P[k]["test"].sha256.values == t.sha256.values).all() for k in P)
            y = t.label.values
            fm, ben = (t.family.values == fam) & (y == 1), y == 0
            dec = {k: P[k]["test"].score.values >= thr[k] for k in P}
            s_sc, d_sc = t.score.values, P["D"]["test"].score.values
            r = {"rodina": fam, "seed": seed, "n": int(fm.sum())}
            # 1) TPR vynechanej rodiny, komplementarita a horná hranica kombinácie dvoch rozhodnutí
            for k in P:
                r[f"tpr_{k}"] = dec[k][fm].mean()
            r["tpr_S_alebo_D"] = (dec["S"] | dec["D"])[fm].mean()
            r["fpr_S"], r["fpr_S_alebo_D"] = dec["S"][ben].mean(), (dec["S"] | dec["D"])[ben].mean()
            miss = fm & ~dec["S"]
            r["D_opraví_z_minutých_S"] = dec["D"][miss].mean() if miss.any() else np.nan
            for tag, split in (("jan", "holdout"),):
                h = {k: P[k][split] for k in P}
                for k in P:
                    r[f"tpr_{k}_{tag}"] = (h[k].score.values >= thr[k]).mean()
                r[f"tpr_S_alebo_D_{tag}"] = ((h["S"].score.values >= thr["S"]) | (h["D"].score.values >= thr["D"])).mean()
            # 2) oddeliteľnosť (ROC-AUC vynechaná rodina vs. neškodné testu) a posun prahu
            sel = fm | ben
            r["auc_S"], r["auc_D"] = roc_auc_score(y[sel], s_sc[sel]), roc_auc_score(y[sel], d_sc[sel])
            for f in (0.01, 0.02):   # ORÁKULUM: prah určený na teste
                tt = threshold_for_fpr(y[sel], s_sc[sel], f)
                r[f"orakulum_tpr_S_pri_FPR_testu_{f:.0%}"] = (s_sc[fm] >= tt).mean()
            # 3) kde ležia chyby: eskalácia pri rozpočte 10 % a schopnosť modelov v eskalovanej oblasti
            sv = P["S"]["validation"].score.values
            cut = np.quantile(np.abs(logit(sv) - logit(thr["S"])), BUDGET)
            esc = np.abs(logit(s_sc) - logit(thr["S"])) <= cut
            r["eskalované"] = esc.mean()
            r["eskalované_z_minutých_S"] = esc[miss].mean() if miss.any() else np.nan
            es = esc & sel
            for k in P:
                r[f"auc_v_eskalovanej_{k}"] = roc_auc_score(y[es], P[k]["test"].score.values[es])
            r["orakulum_dokonalý_2_stupeň"] = ((~esc & dec["S"]) | esc)[fm].mean()   # ORÁKULUM
            rows.append(r)
            if seed == 0:   # 4) podľa výsledku emulácie
                g = emu.reindex(t.sha256.values[fm]).to_numpy()
                for k in ("emulácia ok", "unsupported_api", "malý report"):
                    m = g == k
                    if m.any():
                        subs.append({"rodina": fam, "podskupina": k, "n": int(m.sum()),
                                     "tpr_S": dec["S"][fm][m].mean(), "tpr_D": dec["D"][fm][m].mean()})
    return pd.DataFrame(rows), pd.DataFrame(subs)


def md(df: pd.DataFrame, digits=3) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join(f"{v:.{digits}f}" if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(out)


def main(root: Path):
    df, subs = analyze(root)
    out = root / "comparison" / "v2"
    df.to_csv(out / "analysis_per_family_seed.csv", index=False)
    subs.to_csv(out / "analysis_emulation_subsets.csv", index=False)
    fam = df.drop(columns="seed").groupby("rodina", sort=False).mean().reset_index()
    avg = fam.drop(columns="rodina").mean().to_frame().T.assign(rodina="PRIEMER")
    fam = pd.concat([fam, avg[fam.columns]], ignore_index=True)

    def part(cols):
        return md(fam[["rodina"] + cols])
    L = ["# V2 – analýza príčin (zero-day)", "",
         "> Generované `src/evaluation/v2_analysis.py`. Modely LightGBM z `runs_v2/lofo`, prahy z validácie (FPR 1 %),",
         "> priemer cez seedy 0–2. Stĺpce **orákulum** používajú test (prah na teste, dokonalý druhý stupeň) – sú to iba",
         "> horné hranice na vysvetlenie, nie výsledky metódy. Test vynechanej rodiny = apríl 2022, „jan“ = jej januárové vzorky.", "",
         "## 1. Koľko môže kombinácia statického a dynamického rozhodnutia pridať",
         "S = statický, D = dynamický, H = hybrid; „S alebo D“ = malvér, ak ho označí aspoň jeden (horná hranica pre",
         "každé pravidlo, ktoré kombinuje tieto dve rozhodnutia).", "",
         part(["n", "tpr_S", "tpr_D", "tpr_H", "tpr_S_alebo_D", "D_opraví_z_minutých_S", "fpr_S", "fpr_S_alebo_D"]), "",
         part(["tpr_S_jan", "tpr_D_jan", "tpr_H_jan", "tpr_S_alebo_D_jan"]), "",
         "## 2. Oddeliteľnosť vynechanej rodiny a posun prahu",
         "ROC-AUC = vynechaná rodina vs. neškodné testu (nezávislé od prahu). Orákulum = TPR statického modelu, keby prah",
         "dosiahol na teste FPR 1 % alebo 2 % (prah z validácie dáva na teste FPR iba ~0,5 %).", "",
         part(["auc_S", "auc_D", "tpr_S", "fpr_S", "orakulum_tpr_S_pri_FPR_testu_1%", "orakulum_tpr_S_pri_FPR_testu_2%"]), "",
         f"## 3. Eskalácia pri rozpočte {BUDGET:.0%} (hranica z validácie) a horná hranica kaskády B",
         "ROC-AUC v eskalovanej oblasti = vynechaná rodina vs. neškodné medzi eskalovanými súbormi testu.", "",
         part(["eskalované", "eskalované_z_minutých_S", "auc_v_eskalovanej_S", "auc_v_eskalovanej_D", "auc_v_eskalovanej_H",
               "tpr_S", "orakulum_dokonalý_2_stupeň"]), "",
         "## 4. Vynechaná rodina podľa výsledku emulácie (test, seed 0)", "", md(subs), ""]
    (out / "ANALYSIS.md").write_text("\n".join(L), encoding="utf-8")
    print(f"Analýza: {out / 'ANALYSIS.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("runs_v2"))
    main(ap.parse_args().root)
