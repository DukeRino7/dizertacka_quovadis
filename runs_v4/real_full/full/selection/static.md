# Výber: static

> Generované `src/training/select_best.py` (2026-11-22T20:28:51+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `static/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: static/lightgbm (0.94797); zhodní v rámci sm. odchýlky: ['static/lightgbm', 'static/rf']
- 2) najvyššie ROC-AUC: static/lightgbm (0.99495); zhodní: ['static/lightgbm']

Chýbajúci kandidáti: žiadni

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
            spec                                                     run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       static/lr        runs_v4/real_full/full/static/lr/20261122-184714 0.628654     0.000000   0.968709       0.000000      0.001325
       static/rf        runs_v4/real_full/full/static/rf/20261122-184723 0.946122     0.000418   0.994523       0.000048      0.043721
 static/lightgbm  runs_v4/real_full/full/static/lightgbm/20261122-184829 0.947975     0.002284   0.994953       0.000043      0.205395
static/mlp_small runs_v4/real_full/full/static/mlp_small/20261122-190134 0.916727     0.004834   0.991539       0.000652      0.050523
static/mlp_large runs_v4/real_full/full/static/mlp_large/20261122-190815 0.908593     0.004145   0.991797       0.000319      0.065297
```
