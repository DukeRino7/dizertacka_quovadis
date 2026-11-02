# Kontrolné experimenty – dynamic_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-02T04:36:00+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; (*) = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_full](../../dynamic_ablations/lightgbm_full/20261102-043313/README.md) | 0 | 0.9970 | 0.9972 | +0.0002 | 0.9557 | 0.9547 | -0.0010 | 0.7816 | 0.8400 | +0.0585 | 0.9750 | 0.9744 | -0.0005 | 0.0098 | 0.0098 | +0.0000 |
| [lr_full](../../dynamic_ablations/lr_full/20261102-043439/README.md) | 0 | 0.9941 | 0.9941 | +0.0001 | 0.8814 | 0.8836 | +0.0022 | 0.7396 | 0.7478 | +0.0082 | 0.9346 | 0.9358 | +0.0012 | 0.0098 | 0.0098 | +0.0000 |
| [mlp_large_full](../../dynamic_ablations/mlp_large_full/20261102-043500/README.md) | 0 | 0.9959 | 0.9961 | +0.0002 | 0.9246 | 0.9378 | +0.0132 | 0.7766 | 0.8027 | +0.0262 | 0.9584 | 0.9655 | +0.0072 | 0.0098 | 0.0097 | -0.0001 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_full](../../dynamic_ablations/lightgbm_full/20261102-043313/README.md) | 0 | 0.9560 | 0.9415 | -0.0145 | 0.5849 | 0.5523 | -0.0327 | 0.3139 | 0.3055 | -0.0084 | 0.7852 | 0.7533 | -0.0319 | 0.0198 | 0.0222 | +0.0024 |
| [lr_full](../../dynamic_ablations/lr_full/20261102-043439/README.md) | 0 | 0.8464 | 0.8475 | +0.0011 | 0.2747 | 0.2688 | -0.0060 | 0.1832 | 0.0619 | -0.1213 | 0.6282 | 0.6314 | +0.0031 | 0.0942 | 0.1349 | +0.0407 |
| [mlp_large_full](../../dynamic_ablations/mlp_large_full/20261102-043500/README.md) | 0 | 0.9276 | 0.9319 | +0.0042 | 0.4963 | 0.4957 | -0.0006 | 0.3251 | 0.3674 | +0.0423 | 0.6858 | 0.7225 | +0.0367 | 0.0145 | 0.0195 | +0.0050 |
