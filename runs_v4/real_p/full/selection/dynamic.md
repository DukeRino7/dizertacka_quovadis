# Výber: dynamic

> Generované `src/training/select_best.py` (2026-11-23T00:18:38+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `dynamic/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: dynamic/lightgbm (0.84009); zhodní v rámci sm. odchýlky: ['dynamic/lightgbm']

Chýbajúci kandidáti: ['dynamic/seq_cnn']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                   run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       dynamic/lr        runs_v4/real_p/full/dynamic/lr/20261122-233312 0.496649     0.000000   0.909977       0.000000      0.000943
       dynamic/rf        runs_v4/real_p/full/dynamic/rf/20261122-233325 0.820576     0.001426   0.975503       0.000099      0.059142
 dynamic/lightgbm  runs_v4/real_p/full/dynamic/lightgbm/20261122-233440 0.840094     0.002740   0.981245       0.000147      0.116936
dynamic/mlp_small runs_v4/real_p/full/dynamic/mlp_small/20261122-234317 0.790594     0.006879   0.973173       0.000315      0.036011
dynamic/mlp_large runs_v4/real_p/full/dynamic/mlp_large/20261122-235153 0.795885     0.012671   0.974524       0.000354      0.099547
  dynamic/seq_cnn                                                   NaN      NaN          NaN        NaN            NaN           NaN
```
