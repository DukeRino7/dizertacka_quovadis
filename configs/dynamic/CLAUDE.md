# configs/dynamic/

Spoločný rebríček modelov pre prístup `dynamic` – **rovnaké modely a priestory hyperparametrov ako `configs/static/`**,
líši sa iba vstup: vektor z API volaní (processed/dynamic/tabular). Spoločné pravidlá: `configs/protocol.yaml`.

| Súbor | Model | Výsledky |
|---|---|---|
| `lr.yaml` | logistická regresia | `runs/dynamic/lr/` |
| `rf.yaml` | Random Forest | `runs/dynamic/rf/` |
| `lightgbm.yaml` | LightGBM | `runs/dynamic/lightgbm/` |
| `mlp_small.yaml` | malé MLP | `runs/dynamic/mlp_small/` |
| `mlp_large.yaml` | veľké MLP | `runs/dynamic/mlp_large/` |

Spustiť až po príprave dynamických dát: `.venv\Scripts\python.exe -m src.training.run_suite --approach dynamic`.
