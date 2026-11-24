# Výber: static

> Generované `src/training/select_best.py` (2026-11-23T00:18:38+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `static/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: static/lightgbm (0.94556); zhodní v rámci sm. odchýlky: ['static/lightgbm']

Chýbajúci kandidáti: žiadni

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
            spec                                                  run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
       static/lr        runs_v4/real_p/full/static/lr/20261122-230905 0.617989     0.000000   0.963188       0.000000      0.001097
       static/rf        runs_v4/real_p/full/static/rf/20261122-230914 0.935097     0.001272   0.993330       0.000076      0.059603
 static/lightgbm  runs_v4/real_p/full/static/lightgbm/20261122-231010 0.945561     0.005603   0.994371       0.000141      0.200608
static/mlp_small runs_v4/real_p/full/static/mlp_small/20261122-231849 0.902646     0.004277   0.990208       0.000413      0.038267
static/mlp_large runs_v4/real_p/full/static/mlp_large/20261122-232356 0.902646     0.012965   0.990754       0.000035      0.218552
```
