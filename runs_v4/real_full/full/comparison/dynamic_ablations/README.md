# Kontrolné experimenty – dynamic_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-22T20:24:35+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; (*) = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261122-201826/README.md) | 0 | 0.9848 | 0.9816 | -0.0032 | 0.8717 | 0.8552 | -0.0165 | 0.7520 | 0.7408 | -0.0112 | 0.9271 | 0.9177 | -0.0095 | 0.0098 | 0.0097 | -0.0001 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261122-201943/README.md) | 0 | 0.9207 | 0.9011 | -0.0197 | 0.5794 | 0.5054 | -0.0739 | 0.4752 | 0.2063 | -0.2689 | 0.7297 | 0.6676 | -0.0620 | 0.0098 | 0.0098 | +0.0000 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261122-201948/README.md) | 0 | 0.9786 | 0.9762 | -0.0024 | 0.8179 | 0.7989 | -0.0190 | 0.6453 | 0.5719 | -0.0734 | 0.8955 | 0.8840 | -0.0116 | 0.0098 | 0.0097 | -0.0001 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261122-202014/README.md) | 0 | 0.9773 | 0.9747 | -0.0026 | 0.8130 | 0.7889 | -0.0241 | 0.6363 | 0.5455 | -0.0908 | 0.8926 | 0.8778 | -0.0148 | 0.0098 | 0.0097 | -0.0001 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261122-202126/README.md) | 0 | 0.9797 | 0.9765 | -0.0032 | 0.8452 | 0.8264 | -0.0188 | 0.7546 | 0.7422 | -0.0124 | 0.9118 | 0.9006 | -0.0112 | 0.0098 | 0.0098 | +0.0000 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261122-202151/README.md) | 0 | 0.9975 | 0.9971 | -0.0004 | 0.9720 | 0.9696 | -0.0023 | 0.9197 | 0.8999 | -0.0198 | 0.9816 | 0.9803 | -0.0013 | 0.0095 | 0.0097 | +0.0002 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261122-202322/README.md) | 0 | 0.9869 | 0.9833 | -0.0036 | 0.8652 | 0.8014 | -0.0638 | 0.5849 | 0.4267 | -0.1583 | 0.9234 | 0.8855 | -0.0379 | 0.0098 | 0.0098 | +0.0000 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261122-202325/README.md) | 0 | 0.9952 | 0.9947 | -0.0005 | 0.9626 | 0.9533 | -0.0093 | 0.8202 | 0.7906 | -0.0296 | 0.9767 | 0.9718 | -0.0049 | 0.0097 | 0.0098 | +0.0001 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261122-202359/README.md) | 0 | 0.9950 | 0.9945 | -0.0005 | 0.9616 | 0.9469 | -0.0147 | 0.7276 | 0.7127 | -0.0149 | 0.9761 | 0.9684 | -0.0077 | 0.0098 | 0.0098 | +0.0000 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261122-202426/README.md) | 0 | 0.9962 | 0.9956 | -0.0006 | 0.9513 | 0.9455 | -0.0058 | 0.8986 | 0.8950 | -0.0036 | 0.9708 | 0.9679 | -0.0029 | 0.0095 | 0.0092 | -0.0004 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261122-201826/README.md) | 0 | 0.9857 | 0.9838 | -0.0019 | 0.8730 | 0.8624 | -0.0106 | 0.7717 | 0.7502 | -0.0215 | 0.9259 | 0.9152 | -0.0107 | 0.0090 | 0.0071 | -0.0019 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261122-201943/README.md) | 0 | 0.9232 | 0.9040 | -0.0192 | 0.5633 | 0.4968 | -0.0665 | 0.4604 | 0.3418 | -0.1187 | 0.7224 | 0.6691 | -0.0532 | 0.0114 | 0.0124 | +0.0010 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261122-201948/README.md) | 0 | 0.9797 | 0.9776 | -0.0021 | 0.8213 | 0.8061 | -0.0152 | 0.6540 | 0.6778 | +0.0238 | 0.8882 | 0.8774 | -0.0108 | 0.0073 | 0.0071 | -0.0002 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261122-202014/README.md) | 0 | 0.9789 | 0.9759 | -0.0030 | 0.8184 | 0.7959 | -0.0224 | 0.6433 | 0.6623 | +0.0189 | 0.8848 | 0.8702 | -0.0146 | 0.0074 | 0.0077 | +0.0003 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261122-202126/README.md) | 0 | 0.9810 | 0.9780 | -0.0031 | 0.8560 | 0.8255 | -0.0304 | 0.7570 | 0.7366 | -0.0204 | 0.9118 | 0.8986 | -0.0132 | 0.0078 | 0.0091 | +0.0013 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261122-202151/README.md) | 0 | 0.9983 | 0.9980 | -0.0002 | 0.9781 | 0.9777 | -0.0004 | 0.9330 | 0.9210 | -0.0120 | 0.9826 | 0.9818 | -0.0008 | 0.0076 | 0.0068 | -0.0008 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261122-202322/README.md) | 0 | 0.9878 | 0.9855 | -0.0023 | 0.8740 | 0.8463 | -0.0277 | 0.6184 | 0.5088 | -0.1096 | 0.9256 | 0.8886 | -0.0370 | 0.0097 | 0.0061 | -0.0035 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261122-202325/README.md) | 0 | 0.9962 | 0.9959 | -0.0003 | 0.9663 | 0.9591 | -0.0072 | 0.8937 | 0.8641 | -0.0296 | 0.9765 | 0.9731 | -0.0035 | 0.0072 | 0.0083 | +0.0011 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261122-202359/README.md) | 0 | 0.9956 | 0.9957 | +0.0001 | 0.9655 | 0.9588 | -0.0067 | 0.8821 | 0.8711 | -0.0111 | 0.9756 | 0.9693 | -0.0063 | 0.0080 | 0.0071 | -0.0009 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261122-202426/README.md) | 0 | 0.9968 | 0.9963 | -0.0005 | 0.9621 | 0.9587 | -0.0034 | 0.9109 | 0.8971 | -0.0139 | 0.9737 | 0.9693 | -0.0044 | 0.0064 | 0.0062 | -0.0002 |
