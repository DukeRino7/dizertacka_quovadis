# Kontrolné experimenty – dynamic_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-23T00:15:14+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; (*) = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261123-001142/README.md) | 0 | 0.9812 | 0.9773 | -0.0039 | 0.8401 | 0.8228 | -0.0173 | 0.7038 | 0.6785 | -0.0253 | 0.9073 | 0.8969 | -0.0104 | 0.0096 | 0.0097 | +0.0002 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261123-001226/README.md) | 0 | 0.9100 | 0.8929 | -0.0171 | 0.4966 | 0.4582 | -0.0384 | 0.3813 | 0.3358 | -0.0455 | 0.6584 | 0.6233 | -0.0351 | 0.0097 | 0.0097 | +0.0000 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261123-001229/README.md) | 0 | 0.9745 | 0.9707 | -0.0038 | 0.7959 | 0.7708 | -0.0250 | 0.6375 | 0.5009 | -0.1366 | 0.8805 | 0.8648 | -0.0157 | 0.0096 | 0.0096 | +0.0001 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261123-001256/README.md) | 0 | 0.9732 | 0.9706 | -0.0026 | 0.7906 | 0.7520 | -0.0386 | 0.5699 | 0.4969 | -0.0730 | 0.8772 | 0.8527 | -0.0245 | 0.0097 | 0.0096 | -0.0001 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261123-001342/README.md) | 0 | 0.9755 | 0.9715 | -0.0040 | 0.8206 | 0.7989 | -0.0216 | 0.7550 | 0.6979 | -0.0570 | 0.8955 | 0.8824 | -0.0131 | 0.0097 | 0.0096 | -0.0001 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261123-001403/README.md) | 0 | 0.9969 | 0.9963 | -0.0006 | 0.9707 | 0.9660 | -0.0047 | 0.8957 | 0.8663 | -0.0294 | 0.9792 | 0.9769 | -0.0024 | 0.0096 | 0.0096 | -0.0001 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261123-001420/README.md) | 0 | 0.9842 | 0.9820 | -0.0022 | 0.8187 | 0.7760 | -0.0427 | 0.5164 | 0.5439 | +0.0275 | 0.8944 | 0.8682 | -0.0262 | 0.0097 | 0.0095 | -0.0003 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261123-001423/README.md) | 0 | 0.9944 | 0.9932 | -0.0013 | 0.9447 | 0.9373 | -0.0074 | 0.7319 | 0.7276 | -0.0044 | 0.9657 | 0.9617 | -0.0040 | 0.0096 | 0.0097 | +0.0002 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261123-001449/README.md) | 0 | 0.9941 | 0.9933 | -0.0008 | 0.9478 | 0.9283 | -0.0195 | 0.7872 | 0.7552 | -0.0320 | 0.9672 | 0.9568 | -0.0104 | 0.0097 | 0.0097 | +0.0000 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261123-001455/README.md) | 0 | 0.9955 | 0.9948 | -0.0006 | 0.9438 | 0.9354 | -0.0083 | 0.8970 | 0.8823 | -0.0147 | 0.9651 | 0.9608 | -0.0043 | 0.0097 | 0.0096 | -0.0002 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261123-001142/README.md) | 0 | 0.9824 | 0.9799 | -0.0025 | 0.8586 | 0.8392 | -0.0194 | 0.7618 | 0.7221 | -0.0397 | 0.9118 | 0.8998 | -0.0120 | 0.0074 | 0.0071 | -0.0003 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261123-001226/README.md) | 0 | 0.9166 | 0.8991 | -0.0175 | 0.5290 | 0.4571 | -0.0719 | 0.3908 | 0.3684 | -0.0224 | 0.6596 | 0.6357 | -0.0239 | 0.0069 | 0.0116 | +0.0047 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261123-001229/README.md) | 0 | 0.9743 | 0.9720 | -0.0024 | 0.8052 | 0.7790 | -0.0262 | 0.6573 | 0.6352 | -0.0221 | 0.8739 | 0.8591 | -0.0148 | 0.0076 | 0.0079 | +0.0003 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261123-001256/README.md) | 0 | 0.9754 | 0.9710 | -0.0045 | 0.8118 | 0.7677 | -0.0441 | 0.6488 | 0.5950 | -0.0538 | 0.8724 | 0.8501 | -0.0223 | 0.0072 | 0.0074 | +0.0002 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261123-001342/README.md) | 0 | 0.9771 | 0.9738 | -0.0033 | 0.8348 | 0.8086 | -0.0262 | 0.7417 | 0.6980 | -0.0437 | 0.8997 | 0.8846 | -0.0151 | 0.0077 | 0.0089 | +0.0012 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261123-001403/README.md) | 0 | 0.9982 | 0.9978 | -0.0004 | 0.9783 | 0.9740 | -0.0043 | 0.9274 | 0.9217 | -0.0057 | 0.9814 | 0.9793 | -0.0021 | 0.0062 | 0.0062 | +0.0000 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261123-001420/README.md) | 0 | 0.9861 | 0.9843 | -0.0019 | 0.8484 | 0.8294 | -0.0190 | 0.5997 | 0.5401 | -0.0596 | 0.9029 | 0.8753 | -0.0275 | 0.0070 | 0.0054 | -0.0016 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261123-001423/README.md) | 0 | 0.9959 | 0.9949 | -0.0010 | 0.9555 | 0.9517 | -0.0038 | 0.8393 | 0.8072 | -0.0321 | 0.9691 | 0.9646 | -0.0045 | 0.0078 | 0.0073 | -0.0005 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261123-001449/README.md) | 0 | 0.9949 | 0.9949 | +0.0000 | 0.9588 | 0.9473 | -0.0115 | 0.8049 | 0.8093 | +0.0045 | 0.9698 | 0.9614 | -0.0083 | 0.0065 | 0.0070 | +0.0004 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261123-001455/README.md) | 0 | 0.9965 | 0.9958 | -0.0007 | 0.9613 | 0.9544 | -0.0069 | 0.8956 | 0.8912 | -0.0043 | 0.9712 | 0.9659 | -0.0053 | 0.0057 | 0.0060 | +0.0003 |
