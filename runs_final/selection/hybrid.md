# Výber: hybrid

> Generované `src/training/select_best.py` (2026-11-02T20:49:29+01:00). Pravidlo: `configs/selection.yaml`, `docs/00_vyskumne_otazky.md`.

**Vybraný: `hybrid/lightgbm`**

Postup:
- 1) najvyššie TPR@FPR1%: hybrid/rf (0.99712); zhodní v rámci sm. odchýlky: ['hybrid/rf', 'hybrid/lightgbm']
- 2) najvyššie ROC-AUC: hybrid/rf (0.99981); zhodní: ['hybrid/rf', 'hybrid/lightgbm']
- 3) najnižší CPU čas na vzorku: hybrid/lightgbm (0.0858 ms)

Chýbajúci kandidáti: žiadni

primary = TPR pri FPR 1 % (validácia), secondary = ROC-AUC (validácia), cpu_ms_batch = CPU čas na vzorku (benchmark)

```
             spec                                          run  primary  primary_std  secondary  secondary_std  cpu_ms_batch
        hybrid/lr         runs_final/hybrid/lr/20261102-044357 0.987961     0.000000   0.998876       0.000000      0.050014
        hybrid/rf         runs_final/hybrid/rf/20261102-044751 0.997124     0.000116   0.999807       0.000003      0.151032
  hybrid/lightgbm   runs_final/hybrid/lightgbm/20261102-052826 0.996790     0.000531   0.999788       0.000026      0.085778
 hybrid/mlp_small  runs_final/hybrid/mlp_small/20261102-063854 0.995519     0.000645   0.999276       0.000194      0.345320
 hybrid/mlp_large  runs_final/hybrid/mlp_large/20261102-064138 0.995653     0.000463   0.999485       0.000018      0.474680
hybrid/two_branch runs_final/hybrid/two_branch/20261102-170657 0.996054     0.000505   0.999432       0.000091     32.450329
```
