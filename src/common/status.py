r"""Prehľad stavu experimentu: ktoré kroky sú hotové, čo je rozpracované a čo nasleduje.

    .venv\Scripts\python.exe -m src.common.status            (alebo scripts\status.ps1)
Číta značky krokov (<RunsDir>\_state\*.done) a dokončené behy modelov (metrics.json).
"""
import json
from pathlib import Path

from .paths import PROJECT_ROOT, RUNS_DIR

# (skript, id kroku, popis, priečinky behov pre počítanie hotových modelov)
PLAN = [
    ("run_static.ps1", [
        ("static_train", "Tréning statických modelov", [f"static/{m}" for m in ("lr", "rf", "lightgbm", "mlp_small", "mlp_large")]),
        ("static_benchmark", "Meranie spotreby – statické", []),
        ("static_importance", "Analýza využívania príznakov", []),
        ("static_ablations", "Kontrolné experimenty (bez podpisu a času)", [f"static_ablations/{m}_no_sig_ts" for m in ("lr", "lightgbm", "mlp_large")]),
        ("static_compare", "Porovnanie statických modelov", []),
    ]),
    ("prepare_dynamic.ps1", [
        ("dyn_download", "Speakeasy dáta (stiahnutie / overenie)", []),
        ("dyn_audit", "Audit dynamických dát  → ROZHODNUTIE (docs/04)", []),
    ]),
    ("run_dynamic_hybrid.ps1", [
        ("dyn_cache", "Cache reportov", []), ("dyn_tabular", "Vektor z API volaní", []), ("dyn_sequence", "Postupnosti API", []),
        ("dyn_train", "Tréning dynamických modelov", [f"dynamic/{m}" for m in ("lr", "rf", "lightgbm", "mlp_small", "mlp_large", "seq_cnn")]),
        ("hyb_train", "Tréning hybridných modelov", [f"hybrid/{m}" for m in ("lr", "rf", "lightgbm", "mlp_small", "mlp_large", "two_branch")]),
        ("dyn_benchmark", "Meranie spotreby – dynamické", []), ("hyb_benchmark", "Meranie spotreby – hybridné", []),
        ("dyn_importance", "Analýza príznakov – dynamické", []), ("hyb_importance", "Analýza príznakov – hybridné", []),
        ("dyn_compare", "Porovnanie dynamických", []), ("hyb_compare", "Porovnanie hybridných", []),
    ]),
    ("run_distillation_cascade.ps1", [
        ("select", "Výber modelov podľa pravidla (učiteľ)", []),
        ("oof_hybrid", "Mäkké označenia – hybridný učiteľ", []), ("oof_static", "Mäkké označenia – statický učiteľ", []),
        ("oof_dynamic", "Mäkké označenia – dynamický učiteľ", []),
        ("stud_static", "Statickí študenti", [f"students_static/{m}" for m in ("mlp_kd", "mlp_nokd", "mlp_kd_modal")]),
        ("stud_dynamic", "Dynamickí študenti", [f"students_dynamic/{m}" for m in ("mlp_kd", "mlp_nokd", "mlp_kd_modal")]),
        ("stud_bench_s", "Meranie spotreby – statickí študenti", []), ("stud_bench_d", "Meranie spotreby – dynamickí študenti", []),
        *[(f"cascade_{v}", f"Kaskáda {v}", []) for v in ("main", "nokd", "modal", "heavy", "baselines")],
        ("final_report", "Záverečné porovnanie (výskumné otázky)", []),
    ]),
]


def _done_models(dirs: list[str]) -> tuple[int, list[str]]:
    done = []
    for d in dirs:
        p = RUNS_DIR / d
        if p.exists() and any((r / "metrics.json").exists() for r in p.iterdir() if r.is_dir()):
            done.append(d.split("/")[-1])
    return len(done), done


def main():
    state = RUNS_DIR / "_state"
    version = (PROJECT_ROOT / "VERSION.txt").read_text(encoding="utf-8").strip() if (PROJECT_ROOT / "VERSION.txt").exists() else "?"
    print(f"Stav experimentu | výsledky: {RUNS_DIR} | verzia kódu: {version}\n")
    next_shown = False
    for script, steps in PLAN:
        n_done = sum((state / f"{sid}.done").exists() for sid, _, _ in steps)
        head = "HOTOVÉ" if n_done == len(steps) else ("ROZPRACOVANÉ" if n_done else "nezačaté")
        print(f"{script}  [{head}, {n_done}/{len(steps)} krokov]")
        for sid, title, dirs in steps:
            mark = state / f"{sid}.done"
            if mark.exists():
                print(f"   [x] {title}  ({mark.read_text(encoding='utf-8-sig').strip()})")
                continue
            extra = ""
            if dirs:
                k, names = _done_models(dirs)
                extra = f"  – hotové modely {k}/{len(dirs)}" + (f": {', '.join(names)}" if names else "")
            arrow = "  <-- ĎALŠÍ KROK" if not next_shown else ""
            next_shown = True
            print(f"   [ ] {title}{extra}{arrow}")
        print()
    if not next_shown:
        print("Všetky kroky V1 sú hotové. Záverečný report: comparison/final/README.md")
    else:
        print("Pokračovanie: spustiť skript s prvým nehotovým krokom (hotové kroky a modely sa preskočia).")


if __name__ == "__main__":
    main()
