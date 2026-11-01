# configs/hybrid/

Spoločný rebríček modelov pre prístup `hybrid` – **rovnaké modely a priestory hyperparametrov ako `configs/static/`**,
líši sa iba vstup: spojenie statického EMBER vektora a dynamického vektora (ranná fúzia). Spoločné pravidlá: `configs/protocol.yaml`.

| Súbor | Model | Výsledky |
|---|---|---|
| `lr.yaml` | logistická regresia | `runs/hybrid/lr/` |
| `rf.yaml` | Random Forest | `runs/hybrid/rf/` |
| `lightgbm.yaml` | LightGBM | `runs/hybrid/lightgbm/` |
| `mlp_small.yaml` | malé MLP | `runs/hybrid/mlp_small/` |
| `mlp_large.yaml` | veľké MLP | `runs/hybrid/mlp_large/` |
| `two_branch.yaml` | dvojvetvová sieť (vrstva B), vstup `hybrid_seq` | `runs/hybrid/two_branch/` |

Spustiť až po príprave dynamických dát: `.venv\Scripts\python.exe -m src.training.run_suite --approach hybrid`.
