# Výber: hybrid

> Generované `src/training/select_best.py` (2026-11-23T20:26:54+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `hybrid/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: hybrid/lightgbm (0.96026); zhodní v rámci sm. odchýlky: ['hybrid/lightgbm']

Chýbajúci kandidáti: ['hybrid/two_branch']

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                                 run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
        hybrid/lr        runs_v4/emu_p/full/hybrid/lr/20261123-195300 0.725220     0.000000   0.978175       0.000000      0.002500
        hybrid/rf        runs_v4/emu_p/full/hybrid/rf/20261123-195313 0.944738     0.001239   0.994648       0.000082      0.025875
  hybrid/lightgbm  runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420 0.960259     0.001667   0.996025       0.000028      0.226665
 hybrid/mlp_small runs_v4/emu_p/full/hybrid/mlp_small/20261123-200627 0.932510     0.009227   0.992542       0.000203      0.103451
 hybrid/mlp_large runs_v4/emu_p/full/hybrid/mlp_large/20261123-200933 0.942740     0.001469   0.993345       0.000083      0.107564
hybrid/two_branch                                                 NaN      NaN          NaN        NaN            NaN           NaN
```
