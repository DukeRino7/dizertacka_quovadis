# Výber: hybrid

> Generované `src/training/select_best.py` (2026-11-23T00:18:38+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `hybrid/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: hybrid/lightgbm (0.97072); zhodní v rámci sm. odchýlky: ['hybrid/lightgbm']

Chýbajúci kandidáti: ['hybrid/two_branch']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                  run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
        hybrid/lr        runs_v4/real_p/full/hybrid/lr/20261122-235738 0.818695     0.000000   0.984246   1.359740e-16      0.002603
        hybrid/rf        runs_v4/real_p/full/hybrid/rf/20261122-235747 0.943798     0.001591   0.995457   1.538566e-05      0.049648
  hybrid/lightgbm  runs_v4/real_p/full/hybrid/lightgbm/20261122-235912 0.970723     0.000705   0.996877   3.660153e-05      0.057506
 hybrid/mlp_small runs_v4/real_p/full/hybrid/mlp_small/20261123-000512 0.947795     0.008466   0.994073   4.888463e-04      0.099025
 hybrid/mlp_large runs_v4/real_p/full/hybrid/mlp_large/20261123-000809 0.944738     0.006362   0.994443   2.624915e-04      0.241054
hybrid/two_branch                                                  NaN      NaN          NaN        NaN            NaN           NaN
```
