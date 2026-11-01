# src/evaluation/ – vyhodnotenie

| Modul | Úloha |
|---|---|
| `metrics.py` | ROC-AUC, PR-AUC, TPR pri FPR, log loss, Brier; pri prahu accuracy, balanced acc., precision, recall, FPR, F1, MCC, matica zámen; detekcia podľa rodiny; prah pre cieľové FPR z validácie |
| `timing.py` | latencia 1 vzorky (CPU 1 vlákno, GPU), priepustnosť (CPU všetky vlákna, GPU), transformácia vstupu zvlášť |
| `plots.py` | jednotný štýl grafov: ROC (log FPR), PR, rozdelenie skóre, matica zámen, rodiny, priebeh učenia, priebeh ladenia |
| `report.py` | README.md behu a prehľad behov modelu (`runs/<prístup>/<model>/CLAUDE.md`) |
| `compare.py` | porovnanie modelov prístupu → `runs/comparison/<prístup>/` (tabuľka, kvalita vs. latencia) |

Plánované: vyhodnotenie kaskády (podiel eskalácií, spoločné chyby pri zhode študentov, prínos veľkého modelu pri nezhode)
a porovnanie prístupov navzájom.
