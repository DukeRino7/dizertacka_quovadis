# src/evaluation/ – vyhodnotenie

| Modul | Úloha |
|---|---|
| `metrics.py` | `at_prevalence`: prepočet na nízku prevalenciu malvéru (téza 2); ROC-AUC, PR-AUC, TPR pri FPR, log loss, Brier; pri prahu accuracy, balanced acc., precision, recall, FPR, F1, MCC, matica zámen; detekcia podľa rodiny; prah pre cieľové FPR z validácie |
| `timing.py` | latencia 1 vzorky (CPU 1 vlákno, GPU), priepustnosť (CPU všetky vlákna, GPU), transformácia vstupu zvlášť |
| `plots.py` | jednotný štýl grafov: ROC (log FPR), PR, rozdelenie skóre, matica zámen, rodiny, priebeh učenia, priebeh ladenia |
| `report.py` | README.md behu a prehľad behov modelu (`runs/<prístup>/<model>/CLAUDE.md`) |
| `resources.py` | monitor spotreby počas inferencie: CPU čas, vyťaženie CPU, RAM, vyťaženie/pamäť/energia GPU (iba súhrny) |
| `benchmark.py` | **oficiálne meranie spotreby pri inferencii** z uložených modelov → `benchmark.json` v behu (spúšťať na nezaťaženom PC) |
| `feature_importance.py` | ktoré príznaky modely využívajú: permutácia skupín a sledovaných príznakov (všetky modely), SHAP/gain (LightGBM), koeficienty (LR); iba validácia → `importance/` v behu + `runs/comparison/<prístup>/IMPORTANCE.md` |
| `compare_ablations.py` | kontrolné experimenty vs. pôvodný model → `runs/comparison/<priečinok ablácií>/` |
| `final_report.py` | záverečné porovnanie k výskumným otázkam (vybrané modely, študenti, kaskády, fúzia, nároky) → `runs/comparison/final/` |
| `subset_analysis.py` | výsledky podľa výsledku emulácie (malé reporty, `unsupported_api`, ostatné) → `runs/comparison/subsets/` |
| `compare.py` | porovnanie modelov prístupu → `runs/comparison/<prístup>/` (tabuľka, kvalita vs. latencia) |

Plánované: vyhodnotenie kaskády (podiel eskalácií, spoločné chyby pri zhode študentov, prínos veľkého modelu pri nezhode)
a porovnanie prístupov navzájom.
