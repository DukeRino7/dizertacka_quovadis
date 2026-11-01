# src/ – zdrojový kód

| Priečinok | Úloha |
|---|---|
| `common/` | spoločné pomôcky: načítanie konfigurácie, seed, cesty, meranie času a zdrojov, zápis behu |
| `data/` | audit dát, spoločný index, rozdelenie, tvorba cache v `processed/`, načítanie dát pre modely |
| `models/` | definície modelov rozdelené podľa prístupu (static, dynamic, hybrid, students_static, students_dynamic) |
| `training/` | trénovacie postupy vrátane destilácie vedomostí |
| `evaluation/` | metriky, meranie inferencie a výpočtových nárokov, grafy, porovnania |
| `cascade/` | finálna kaskáda: dvaja študenti → pri nezhode veľký hybridný model |

Zásady:
- Každý model sa dá pridať novým súborom v `models/<prístup>/` a konfiguráciou v `configs/<prístup>/`
  bez zásahu do ostatných modelov.
- Modely jedného prístupu majú rovnaké rozhranie (trénovanie, predikcia skóre), aby ich `evaluation/`
  a `cascade/` vedeli používať rovnako.
- Kód nikdy nezapisuje do `data/`. Výstupy idú do `processed/` (dáta) alebo `runs/` (experimenty).
- Test sa nepoužíva na ladenie; prahy a hyperparametre sa vyberajú na validácii.
