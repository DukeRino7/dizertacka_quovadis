# configs/cascade/

Varianty kaskády. Kľúče: `name` (= priečinok v `runs/cascade/`), `components.static|dynamic|hybrid`:
`'<prístup>/<model>'` (posledný dokončený beh), `auto:<skupina>` (model vybraný pravidlom, `runs/selection/`) alebo cesta k behu.

| Súbor | Študenti / modely | Hybrid | Účel |
|---|---|---|---|
| `main.yaml` | `mlp_kd` (destilácia z hybridu) | `auto:hybrid` | **hlavný výsledok** (otázka 4) |
| `nokd.yaml` | `mlp_nokd` (bez destilácie) | `auto:hybrid` | prínos destilácie v kaskáde |
| `modal.yaml` | `mlp_kd_modal` (učiteľ rovnakej modality) | `auto:hybrid` | variant A |
| `heavy.yaml` | `mlp_kd` | `hybrid/two_branch` | kaskáda s najťažším hybridom (doplnková analýza) |
| `baselines.yaml` | `auto:static`, `auto:dynamic` | `auto:hybrid` | referencia bez študentov |

Spustenie: `.venv\Scripts\python.exe -m src.cascade.evaluate --config configs/cascade/<variant>.yaml`.
