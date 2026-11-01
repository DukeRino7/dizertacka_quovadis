# src/training/ – trénovanie a destilácia

| Modul | Úloha |
|---|---|
| `run_tabular.py` | jeden experiment rebríčka: transformácia (fit na train) → ladenie Optuna na validácii → finálne modely s viacerými seedmi → metriky, časy, grafy, README |
| `run_suite.py` | celá sada modelov jedného prístupu za sebou + porovnanie |
| `run_ablations.py` | všetky kontrolné experimenty z `configs/<priečinok>/` + porovnanie s pôvodnými modelmi |
| `teacher_oof.py` | mäkké označenia učiteľa na tréningu krížovo (5 častí, hyperparametre z behu učiteľa) → `runs/teachers/<prístup>_<model>/` |
| `search_space.py` | priestor hyperparametrov z YAML → návrhy Optuna |

Spustenie: `.venv\Scripts\python.exe -m src.training.run_tabular --config configs/static/lr.yaml`
(`--smoke --runs-root <dočasný priečinok>` = rýchla kontrola pipeline na malej podvzorke, nie experiment).

Voliteľné kľúče konfigurácie: `exclude_features` (vynechané príznaky), `params_from: static/lightgbm`
(prevzatie hyperparametrov z posledného behu bez ladenia), `results_approach` (iný priečinok v `runs/`).

Pravidlá (`configs/protocol.yaml`, `docs/03_protokol_a_modely.md`):
- Všetky učené transformácie a destilácia iba na tréningovej časti.
- Validácia slúži na výber hyperparametrov, prahov a zastavenie tréningu. Test sa tu nepoužíva na rozhodnutia.
- Čas tréningu sa meria a ukladá samostatne od inferencie a prípravy vstupu.
- Destilácia vedomostí (dohodnuté, `docs/05`): študent = MLP so stratou α·skutočné + (1−α)·T²·učiteľ; konfigurácia
  `distillation.teacher` → spúšťač načíta mäkké označenia z `runs/teachers/` a zarovná ich podľa SHA-256.
