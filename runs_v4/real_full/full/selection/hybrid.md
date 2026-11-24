# Výber: hybrid

> Generované `src/training/select_best.py` (2026-11-22T20:28:51+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `hybrid/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: hybrid/lightgbm (0.97197); zhodní v rámci sm. odchýlky: ['hybrid/lightgbm']

Chýbajúci kandidáti: ['hybrid/two_branch']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                     run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
        hybrid/lr        runs_v4/real_full/full/hybrid/lr/20261122-195001 0.865185     0.000000   0.986933   1.359740e-16      0.002602
        hybrid/rf        runs_v4/real_full/full/hybrid/rf/20261122-195013 0.951276     0.000608   0.996194   7.677532e-05      0.020716
  hybrid/lightgbm  runs_v4/real_full/full/hybrid/lightgbm/20261122-195127 0.971974     0.000483   0.997530   7.542471e-06      0.178721
 hybrid/mlp_small runs_v4/real_full/full/hybrid/mlp_small/20261122-200826 0.961585     0.001345   0.994985   3.151191e-04      0.105233
 hybrid/mlp_large runs_v4/real_full/full/hybrid/mlp_large/20261122-201300 0.962632     0.003116   0.995247   1.683044e-04      0.114761
hybrid/two_branch                                                     NaN      NaN          NaN        NaN            NaN           NaN
```
