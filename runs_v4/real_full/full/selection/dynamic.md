# Výber: dynamic

> Generované `src/training/select_best.py` (2026-11-22T20:28:51+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `dynamic/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: dynamic/lightgbm (0.87171); zhodní v rámci sm. odchýlky: ['dynamic/lightgbm']

Chýbajúci kandidáti: ['dynamic/seq_cnn']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                      run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       dynamic/lr        runs_v4/real_full/full/dynamic/lr/20261122-191725 0.579367     0.000000   0.920718       0.000000      0.001012
       dynamic/rf        runs_v4/real_full/full/dynamic/rf/20261122-191738 0.845212     0.004201   0.979750       0.000096      0.065091
 dynamic/lightgbm  runs_v4/real_full/full/dynamic/lightgbm/20261122-191914 0.871708     0.004064   0.984801       0.000045      0.240969
dynamic/mlp_small runs_v4/real_full/full/dynamic/mlp_small/20261122-193213 0.812998     0.001509   0.977333       0.000217      0.040037
dynamic/mlp_large runs_v4/real_full/full/dynamic/mlp_large/20261122-194320 0.817911     0.003280   0.978607       0.000118      0.072415
  dynamic/seq_cnn                                                      NaN      NaN          NaN        NaN            NaN           NaN
```
