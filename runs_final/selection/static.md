# Výber: static

> Generované `src/training/select_best.py` (2026-11-02T20:49:29+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `static/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: static/lightgbm (0.99779); zhodní v rámci sm. odchýlky: ['static/lightgbm']

Chýbajúci kandidáti: žiadni

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
            spec                                         run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       static/lr        runs_final/static/lr/20261101-213555 0.983949 0.000000e+00   0.998593       0.000000      0.027260
       static/rf        runs_final/static/rf/20261101-213728 0.995118 1.158407e-04   0.999779       0.000008      0.099034
 static/lightgbm  runs_final/static/lightgbm/20261101-215345 0.997793 1.359740e-16   0.999834       0.000004      0.678564
static/mlp_small runs_final/static/mlp_small/20261101-235005 0.991105 2.839871e-03   0.999033       0.000280      0.295351
static/mlp_large runs_final/static/mlp_large/20261101-235239 0.995385 3.475222e-04   0.999539       0.000061      0.360797
```
