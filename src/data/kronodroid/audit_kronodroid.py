"""Audit KronoDroid CSV (V4, iba čítanie): štruktúra, označenia, SHA-256, duplicity, chýbajúce hodnoty,
prekrytie emulátora a skutočného zariadenia, dátumy, rodiny a stĺpce podobné označeniu.

Nič sa tu nerozhoduje; zistenia slúžia ako podklad pre docs/18 (rozhodnutia sa zapíšu pred trénovaním).

Spustenie z koreňa projektu:
    .venv\\Scripts\\python.exe -m src.data.kronodroid.audit_kronodroid
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.config import load_config
from src.common.paths import rel, resolve
from src.common.provenance import describe_files, environment, git_info, now_iso, sha256_file, write_json

SUBSETS = ["emulator", "real_device"]


def load_subset(cfg: dict, subset: str) -> pd.DataFrame:
    """Načíta obe triedy podmnožiny a zjednotí názvy dátumových stĺpcov na date_first / date_last."""
    raw = resolve(cfg["raw_dir"])
    parts = []
    for cls, fname in cfg["files"][subset].items():
        d = pd.read_csv(raw / fname, low_memory=False)
        d["_file"] = fname
        parts.append(d)
    d = pd.concat(parts, ignore_index=True)
    first, last = cfg["columns"]["dates"][subset]
    d = d.rename(columns={first: "date_first", last: "date_last"})
    d["sha"] = d["sha256"].astype(str).str.lower()
    for c in ["date_first", "date_last"]:
        d[c + "_dt"] = pd.to_datetime(d[c], format="%m/%d/%Y", errors="coerce")
    return d.copy()


def column_groups(d: pd.DataFrame, cfg: dict) -> dict:
    cols = list(d.columns)
    c = cfg["columns"]
    i_dyn = cols.index(c["dynamic_last"])
    i_sha = cols.index("sha256")
    dynamic = cols[2:i_dyn + 1]
    permissions = cols[i_dyn + 1:i_sha]
    meta = [x for x in c["static_metadata"] if x in cols]
    return {"dynamic": dynamic, "permissions": permissions, "static_metadata": meta,
            "static_metadata_missing": [x for x in c["static_metadata"] if x not in cols]}


def md_table(df: pd.DataFrame) -> str:
    df = df.reset_index() if df.index.name or not isinstance(df.index, pd.RangeIndex) else df
    head = "| " + " | ".join(map(str, df.columns)) + " |\n|" + "---|" * len(df.columns) + "\n"
    return head + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in df.itertuples(index=False))


def audit_subset(d: pd.DataFrame, g: dict, cfg: dict) -> dict:
    lab = cfg["columns"]["label"]
    fam = cfg["columns"]["family"]
    static = g["permissions"] + g["static_metadata"]
    feats = g["dynamic"] + static
    sha_ok = d["sha256"].astype(str).str.fullmatch("[0-9a-fA-F]{64}")
    both = set(d.loc[d[lab] == 0, "sha"]) & set(d.loc[d[lab] == 1, "sha"])
    na = d[feats + [fam]].isna().sum()
    dyn_sum = d[g["dynamic"][:-1]].sum(axis=1)
    groups = d.groupby(feats, dropna=False)[lab].nunique()
    r = {
        "rows": len(d),
        "by_label": d[lab].value_counts().sort_index().to_dict(),
        "label_matches_file": int(((d["_file"].str.contains("malware")) == (d[lab] == 1)).sum()),
        "sha_valid": int(sha_ok.sum()),
        "sha_unique": int(d["sha"].nunique()),
        "sha_in_both_classes": len(both),
        "n_dynamic": len(g["dynamic"]), "n_permissions": len(g["permissions"]),
        "n_static_metadata": len(g["static_metadata"]),
        "static_metadata_missing": g["static_metadata_missing"],
        "na_by_column": {k: int(v) for k, v in na[na > 0].items()},
        "nr_syscalls_zero": int((d["nr_syscalls"] == 0).sum()),
        "nr_syscalls_eq_sum": int((dyn_sum == d["nr_syscalls"]).sum()),
        "nr_syscalls_median_by_label": d.groupby(lab)["nr_syscalls"].median().to_dict(),
        "dup_rows_all_features": int(d.duplicated(feats).sum()),
        "dup_rows_static": int(d.duplicated(static).sum()),
        "dup_rows_permissions": int(d.duplicated(g["permissions"]).sum()),
        "unique_static_vectors": int(len(d) - d.duplicated(static).sum()),
        "feature_groups_conflicting_label": int((groups > 1).sum()),
        "package_unique": int(d["Package"].nunique()),
        "benign_with_family": int(d.loc[d[lab] == 0, fam].notna().sum()),
        "malware_without_family": int(d.loc[d[lab] == 1, fam].isna().sum()),
        "n_families": int(d.loc[d[lab] == 1, fam].nunique()),
    }
    dr = d["Detection_Ratio"]
    r["detection_ratio"] = {
        str(k): {"min": round(float(s.min()), 3), "median": round(float(s.median()), 3),
                 "max": round(float(s.max()), 3), "share_gt0": round(float((s > 0).mean()), 4)}
        for k, s in dr.groupby(d[lab])}
    # dátumy: koľko je neplatných, 1980 (predvolený dátum v ZIP), budúcich
    dates = {}
    for c in ["date_first", "date_last"]:
        s = d[c + "_dt"]
        dates[c] = {"unparsed": int(s.isna().sum()), "year_1980": int((s.dt.year == 1980).sum()),
                    "before_2008": int((s.dt.year < 2008).sum()), "after_2020": int((s.dt.year > 2020).sum()),
                    "min": str(s.min().date()), "max": str(s.max().date())}
    r["dates"] = dates
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/kronodroid/data.yaml")
    args = ap.parse_args()
    t0 = time.perf_counter()
    cfg = load_config(args.config)
    out = resolve(cfg["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    lab, fam = cfg["columns"]["label"], cfg["columns"]["family"]

    # integrita stiahnutých ZIP voči konfigurácii
    zdir = resolve(cfg["raw_dir"]).parent / "zip"
    zip_check = {n: sha256_file(zdir / n) == h for n, h in cfg["source"]["zip_sha256"].items()}

    D, G, R = {}, {}, {}
    for s in SUBSETS:
        D[s] = load_subset(cfg, s)
        G[s] = column_groups(D[s], cfg)
        R[s] = audit_subset(D[s], G[s], cfg)

    # prekrytie podmnožín podľa SHA-256
    E = D["emulator"].drop_duplicates("sha").set_index("sha")
    Rd = D["real_device"].drop_duplicates("sha").set_index("sha")
    inter = sorted(set(E.index) & set(Rd.index))
    static = G["emulator"]["permissions"] + [c for c in G["emulator"]["static_metadata"]
                                             if c in G["real_device"]["static_metadata"]]
    same_static = (E.loc[inter, static].fillna(-1).values == Rd.loc[inter, static].fillna(-1).values).all(axis=1)
    same_fam = (E.loc[inter, fam].fillna("") == Rd.loc[inter, fam].fillna("")).values
    same_date = (E.loc[inter, "date_last"].fillna("") == Rd.loc[inter, "date_last"].fillna("")).values
    dyn = G["emulator"]["dynamic"]
    overlap = {
        "both": len(inter), "emulator_only": len(set(E.index) - set(Rd.index)),
        "real_only": len(set(Rd.index) - set(E.index)),
        "both_by_label": E.loc[inter, lab].value_counts().sort_index().to_dict(),
        "label_agree": int((E.loc[inter, lab] == Rd.loc[inter, lab]).sum()),
        "static_identical": int(same_static.sum()), "family_identical": int(same_fam.sum()),
        "date_last_identical": int(same_date.sum()),
        "dynamic_columns_same": G["emulator"]["dynamic"] == G["real_device"]["dynamic"],
        "dynamic_identical": int((E.loc[inter, dyn].values == Rd.loc[inter, dyn].values).all(axis=1).sum()),
        "nr_syscalls_median": {"emulator": float(E.loc[inter, "nr_syscalls"].median()),
                               "real_device": float(Rd.loc[inter, "nr_syscalls"].median())},
        "nr_syscalls_spearman": float(E.loc[inter, "nr_syscalls"].rank().corr(Rd.loc[inter, "nr_syscalls"].rank())),
    }

    # roky podľa triedy (date_last; platné roky 2008–2020) a rodiny
    tabs = {}
    for s in SUBSETS:
        d = D[s]
        y = d["date_last_dt"].dt.year
        y = y.where(y.between(2008, 2020)).astype("Int64").astype(str).replace("<NA>", "neplatný")
        tabs[f"years_{s}"] = pd.crosstab(y, d[lab].map({0: "benign", 1: "malware"}))
        tabs[f"years_{s}"].to_csv(out / f"years_by_label_{s}.csv")
        f = d.loc[d[lab] == 1, fam].fillna("(bez rodiny)").value_counts()
        f.rename("count").to_csv(out / f"families_{s}.csv")
        R[s]["families_ge"] = {k: int((f >= k).sum()) for k in [50, 100, 500, 1000]}
        tabs[f"fam_{s}"] = f.head(15).rename("počet").to_frame()

    summary = {"created": now_iso(), "zip_sha256_ok": zip_check, "subsets": R, "overlap": overlap,
               "duration_s": round(time.perf_counter() - t0, 1), "config": cfg, "git": git_info(),
               "environment": environment()}
    write_json(summary, out / "audit_summary.json")

    def row(key, fmt=str):
        return " | ".join(fmt(R[s][key]) for s in SUBSETS)

    e, r = R["emulator"], R["real_device"]
    text = f"""# Audit KronoDroid

> Generované `src/data/kronodroid/audit_kronodroid.py` ({now_iso()}). Iba popis, rozhodnutia patria do docs/18.
> Zdroj {cfg['source']['repo']} (commit `{cfg['source']['commit'][:7]}`), ZIP súbory sedia s konfiguráciou: {all(zip_check.values())}.

## 1. Základ
| | emulátor | skutočné zariadenie |
|---|---|---|
| riadky | {row('rows')} |
| benign / malware | {e['by_label'].get(0)} / {e['by_label'].get(1)} | {r['by_label'].get(0)} / {r['by_label'].get(1)} |
| označenie sedí so súborom | {row('label_matches_file')} |
| platné SHA-256 / unikátne | {e['sha_valid']} / {e['sha_unique']} | {r['sha_valid']} / {r['sha_unique']} |
| SHA-256 v oboch triedach | {row('sha_in_both_classes')} |
| dynamické stĺpce (systémové volania vrátane nr_syscalls) | {row('n_dynamic')} |
| oprávnenia a ich súčty | {row('n_permissions')} |
| statické metadáta (počty komponentov, veľkosť) | {row('n_static_metadata')} |
| chýbajúce metadáta | {row('static_metadata_missing')} |
| nr_syscalls = 0 | {row('nr_syscalls_zero')} |
| nr_syscalls = súčet volaní | {row('nr_syscalls_eq_sum')} |
| medián nr_syscalls benign / malware | {e['nr_syscalls_median_by_label'][0]:.0f} / {e['nr_syscalls_median_by_label'][1]:.0f} | {r['nr_syscalls_median_by_label'][0]:.0f} / {r['nr_syscalls_median_by_label'][1]:.0f} |
| rodiny malvéru | {row('n_families')} |
| malvér bez rodiny | {row('malware_without_family')} |
| **benign s vyplnenou rodinou** | {row('benign_with_family')} |
| unikátne názvy balíkov | {row('package_unique')} |

Chýbajúce hodnoty (stĺpec: počet): emulátor {e['na_by_column']}; zariadenie {r['na_by_column']}.

## 2. Duplicity
| | emulátor | skutočné zariadenie |
|---|---|---|
| duplicitné riadky vo všetkých príznakoch | {row('dup_rows_all_features')} |
| duplicitné riadky v statických príznakoch | {row('dup_rows_static')} |
| unikátne statické vektory | {row('unique_static_vectors')} |
| duplicitné riadky iba v oprávneniach | {row('dup_rows_permissions')} |
| skupiny rovnakých príznakov s oboma triedami | {row('feature_groups_conflicting_label')} |

## 3. Prekrytie emulátora a skutočného zariadenia (SHA-256)
- v oboch: **{overlap['both']}** (benign/malware {overlap['both_by_label']}), iba emulátor {overlap['emulator_only']}, iba zariadenie {overlap['real_only']}
- zhodné označenie {overlap['label_agree']}, zhodné statické príznaky {overlap['static_identical']}, zhodná rodina {overlap['family_identical']}, zhodný dátum {overlap['date_last_identical']}
- rovnaké dynamické stĺpce: {overlap['dynamic_columns_same']}; úplne zhodné dynamické vektory {overlap['dynamic_identical']}
- medián nr_syscalls na prekrytí: emulátor {overlap['nr_syscalls_median']['emulator']:.0f}, zariadenie {overlap['nr_syscalls_median']['real_device']:.0f}; Spearman {overlap['nr_syscalls_spearman']:.3f}

## 4. Stĺpce z VirusTotal (podobné označeniu)
Detection_Ratio podľa triedy: emulátor {e['detection_ratio']}; zariadenie {r['detection_ratio']}.

## 5. Dátumy (dátumy súborov vo vnútri APK, nie prvé objavenie)
emulátor {e['dates']}

zariadenie {r['dates']}

### Roky podľa triedy (date_last), emulátor
{md_table(tabs['years_emulator'])}

### Roky podľa triedy (date_last), skutočné zariadenie
{md_table(tabs['years_real_device'])}

## 6. Rodiny
Počet rodín s aspoň N vzorkami: emulátor {e['families_ge']}; zariadenie {r['families_ge']}.

### Najčastejšie rodiny, skutočné zariadenie
{md_table(tabs['fam_real_device'])}
"""
    (out / "AUDIT.md").write_text(text, encoding="utf-8")
    write_json({"script": "src/data/kronodroid/audit_kronodroid.py", "created": now_iso(), "git": git_info(),
                "inputs": describe_files(sorted(resolve(cfg["raw_dir"]).glob("*.csv"))),
                "outputs": describe_files([out / "AUDIT.md", out / "audit_summary.json"])},
               out / "manifest.json")
    print(f"hotovo za {time.perf_counter() - t0:.0f} s -> {rel(out)}")


if __name__ == "__main__":
    main()
