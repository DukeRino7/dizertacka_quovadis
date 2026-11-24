# Výber: dynamic

> Generované `src/training/select_best.py` (2026-11-23T20:26:54+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `dynamic/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: dynamic/lightgbm (0.84621); zhodní v rámci sm. odchýlky: ['dynamic/lightgbm']

Chýbajúci kandidáti: ['dynamic/seq_cnn']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                  run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       dynamic/lr        runs_v4/emu_p/full/dynamic/lr/20261123-191800 0.381305 6.798700e-17   0.876493   1.359740e-16      0.000917
       dynamic/rf        runs_v4/emu_p/full/dynamic/rf/20261123-191811 0.782363 3.364865e-03   0.976256   7.632933e-05      0.061450
 dynamic/lightgbm  runs_v4/emu_p/full/dynamic/lightgbm/20261123-191933 0.846208 2.202821e-03   0.980895   2.365760e-04      0.634992
dynamic/mlp_small runs_v4/emu_p/full/dynamic/mlp_small/20261123-193925 0.750735 1.150763e-02   0.967152   7.510527e-04      0.037769
dynamic/mlp_large runs_v4/emu_p/full/dynamic/mlp_large/20261123-194626 0.766961 5.713124e-03   0.968449   6.734511e-04      0.088025
  dynamic/seq_cnn                                                  NaN      NaN          NaN        NaN            NaN           NaN
```
