# configs/static/

Statické modely spoločného rebríčka. Spoločné pravidlá: `configs/protocol.yaml`.

| Súbor | Model | Výsledky |
|---|---|---|
| `lr.yaml` | logistická regresia | `runs/static/lr/` |
| `rf.yaml` | Random Forest | `runs/static/rf/` |
| `lightgbm.yaml` | LightGBM | `runs/static/lightgbm/` |
| `mlp_small.yaml` | malé MLP | `runs/static/mlp_small/` |
| `mlp_large.yaml` | veľké MLP | `runs/static/mlp_large/` |

Kľúče: `name` (= priečinok v runs), `approach`, `model` (trieda v `src/models/tabular`), `search_space`
(ladí sa), `fixed_params` (neladí sa), `smoke_overrides` (iba pre `--smoke`).
