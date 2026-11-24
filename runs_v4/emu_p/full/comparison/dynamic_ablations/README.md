# Kontrolné experimenty – dynamic_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-23T20:20:48+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; (*) = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261123-201347/README.md) | 0 | 0.9809 | 0.9776 | -0.0033 | 0.8462 | 0.8234 | -0.0228 | 0.5045 | 0.6201 | +0.1156 | 0.9108 | 0.8973 | -0.0135 | 0.0097 | 0.0096 | -0.0001 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261123-201614/README.md) | 0 | 0.8765 | 0.8099 | -0.0666 | 0.3813 | 0.1824 | -0.1989 | 0.1079 | 0.0434 | -0.0646 | 0.5473 | 0.3054 | -0.2420 | 0.0097 | 0.0097 | +0.0000 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261123-201617/README.md) | 0 | 0.9684 | 0.9617 | -0.0067 | 0.7670 | 0.7118 | -0.0551 | 0.3753 | 0.2520 | -0.1233 | 0.8623 | 0.8259 | -0.0365 | 0.0096 | 0.0097 | +0.0001 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261123-201651/README.md) | 0 | 0.9672 | 0.9587 | -0.0084 | 0.7507 | 0.6772 | -0.0735 | 0.2554 | 0.2499 | -0.0055 | 0.8518 | 0.8017 | -0.0501 | 0.0096 | 0.0097 | +0.0001 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261123-201749/README.md) | 0 | 0.9763 | 0.9709 | -0.0054 | 0.7824 | 0.7485 | -0.0339 | 0.6218 | 0.6119 | -0.0099 | 0.8720 | 0.8504 | -0.0216 | 0.0097 | 0.0096 | -0.0001 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261123-201810/README.md) | 0 | 0.9960 | 0.9960 | -0.0000 | 0.9603 | 0.9610 | +0.0007 | 0.8663 | 0.8573 | -0.0091 | 0.9738 | 0.9742 | +0.0004 | 0.0097 | 0.0096 | -0.0001 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261123-201947/README.md) | 0 | 0.9782 | 0.9707 | -0.0074 | 0.7252 | 0.6554 | -0.0698 | 0.4451 | 0.2303 | -0.2148 | 0.8349 | 0.7863 | -0.0486 | 0.0097 | 0.0095 | -0.0003 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261123-201950/README.md) | 0 | 0.9933 | 0.9921 | -0.0012 | 0.9427 | 0.9300 | -0.0127 | 0.6830 | 0.7255 | +0.0424 | 0.9646 | 0.9578 | -0.0068 | 0.0097 | 0.0097 | +0.0000 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261123-202022/README.md) | 0 | 0.9925 | 0.9919 | -0.0006 | 0.9325 | 0.9202 | -0.0123 | 0.5912 | 0.5131 | -0.0781 | 0.9591 | 0.9525 | -0.0066 | 0.0097 | 0.0097 | +0.0000 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261123-202038/README.md) | 0 | 0.9946 | 0.9939 | -0.0007 | 0.9447 | 0.9345 | -0.0102 | 0.8039 | 0.7601 | -0.0437 | 0.9658 | 0.9603 | -0.0055 | 0.0095 | 0.0096 | +0.0001 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [dyn_lightgbm_norm](../../dynamic_ablations/dyn_lightgbm_norm/20261123-201347/README.md) | 0 | 0.9780 | 0.9752 | -0.0028 | 0.8488 | 0.8227 | -0.0261 | 0.7359 | 0.7165 | -0.0194 | 0.9071 | 0.8907 | -0.0163 | 0.0080 | 0.0082 | +0.0002 |
| [dyn_lr_norm](../../dynamic_ablations/dyn_lr_norm/20261123-201614/README.md) | 0 | 0.8740 | 0.8071 | -0.0669 | 0.3739 | 0.2052 | -0.1687 | 0.1237 | 0.1014 | -0.0224 | 0.5440 | 0.3173 | -0.2267 | 0.0105 | 0.0062 | -0.0043 |
| [dyn_mlp_large_norm](../../dynamic_ablations/dyn_mlp_large_norm/20261123-201617/README.md) | 0 | 0.9666 | 0.9611 | -0.0055 | 0.7582 | 0.7228 | -0.0354 | 0.4820 | 0.5203 | +0.0383 | 0.8500 | 0.8159 | -0.0342 | 0.0087 | 0.0072 | -0.0016 |
| [dyn_mlp_small_norm](../../dynamic_ablations/dyn_mlp_small_norm/20261123-201651/README.md) | 0 | 0.9651 | 0.9595 | -0.0056 | 0.7413 | 0.7097 | -0.0317 | 0.3551 | 0.5196 | +0.1645 | 0.8350 | 0.7912 | -0.0439 | 0.0086 | 0.0055 | -0.0031 |
| [dyn_rf_norm](../../dynamic_ablations/dyn_rf_norm/20261123-201749/README.md) | 0 | 0.9751 | 0.9689 | -0.0062 | 0.8193 | 0.7795 | -0.0398 | 0.6864 | 0.6455 | -0.0409 | 0.8767 | 0.8516 | -0.0251 | 0.0066 | 0.0066 | +0.0000 |
| [hyb_lightgbm_norm](../../dynamic_ablations/hyb_lightgbm_norm/20261123-201810/README.md) | 0 | 0.9969 | 0.9967 | -0.0002 | 0.9707 | 0.9664 | -0.0043 | 0.9134 | 0.9181 | +0.0046 | 0.9775 | 0.9751 | -0.0024 | 0.0060 | 0.0061 | +0.0001 |
| [hyb_lr_norm](../../dynamic_ablations/hyb_lr_norm/20261123-201947/README.md) | 0 | 0.9798 | 0.9737 | -0.0061 | 0.7530 | 0.7234 | -0.0296 | 0.4313 | 0.2711 | -0.1602 | 0.8381 | 0.7961 | -0.0420 | 0.0089 | 0.0074 | -0.0014 |
| [hyb_mlp_large_norm](../../dynamic_ablations/hyb_mlp_large_norm/20261123-201950/README.md) | 0 | 0.9942 | 0.9939 | -0.0003 | 0.9566 | 0.9518 | -0.0048 | 0.8043 | 0.7701 | -0.0342 | 0.9676 | 0.9619 | -0.0057 | 0.0063 | 0.0063 | -0.0000 |
| [hyb_mlp_small_norm](../../dynamic_ablations/hyb_mlp_small_norm/20261123-202022/README.md) | 0 | 0.9941 | 0.9937 | -0.0003 | 0.9485 | 0.9518 | +0.0033 | 0.7763 | 0.7213 | -0.0550 | 0.9605 | 0.9588 | -0.0017 | 0.0060 | 0.0054 | -0.0006 |
| [hyb_rf_norm](../../dynamic_ablations/hyb_rf_norm/20261123-202038/README.md) | 0 | 0.9956 | 0.9946 | -0.0010 | 0.9547 | 0.9491 | -0.0056 | 0.8897 | 0.8801 | -0.0096 | 0.9680 | 0.9624 | -0.0056 | 0.0066 | 0.0065 | -0.0001 |
