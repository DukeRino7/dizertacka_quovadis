# Výber: dynamic

> Generované `src/training/select_best.py` (2026-11-02T20:49:29+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `dynamic/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: dynamic/rf (0.95626); zhodní v rámci sm. odchýlky: ['dynamic/rf', 'dynamic/lightgbm']
- 2) najvyššie ROC-AUC: dynamic/lightgbm (0.99704); zhodní: ['dynamic/lightgbm']

Chýbajúci kandidáti: žiadni

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                          run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       dynamic/lr        runs_final/dynamic/lr/20261102-002602 0.881421     0.000000   0.994054       0.000000      0.022142
       dynamic/rf        runs_final/dynamic/rf/20261102-003041 0.956260     0.000348   0.996937       0.000053      0.155778
 dynamic/lightgbm  runs_final/dynamic/lightgbm/20261102-003953 0.955725     0.001969   0.997040       0.000012      0.426932
dynamic/mlp_small runs_final/dynamic/mlp_small/20261102-005611 0.927769     0.017210   0.996080       0.000150      0.323102
dynamic/mlp_large runs_final/dynamic/mlp_large/20261102-005920 0.924559     0.016335   0.995901       0.000059      0.358256
  dynamic/seq_cnn   runs_final/dynamic/seq_cnn/20261102-010741 0.949104     0.000579   0.996909       0.000124     18.152719
```
