# Kontrolné experimenty – static_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-01T19:33:14+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; \* = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1* pôvodný | F1* bez | Δ | FPR* pôvodný | FPR* bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_no_sig_ts](../../static_ablations/lightgbm_no_sig_ts/20261101-191319/README.md) | 4 | 0.9998 | 0.9998 | -0.0001 | 0.9978 | 0.9966 | -0.0012 | 0.9900 | 0.9838 | -0.0062 | 0.9967 | 0.9962 | -0.0005 | 0.0089 | 0.0085 | -0.0004 |
| [lr_no_sig_ts](../../static_ablations/lr_no_sig_ts/20261101-193217/README.md) | 4 | 0.9986 | 0.9981 | -0.0005 | 0.9839 | 0.9799 | -0.0040 | 0.8285 | 0.8136 | -0.0148 | 0.9896 | 0.9876 | -0.0020 | 0.0094 | 0.0094 | +0.0000 |
| [mlp_large_no_sig_ts](../../static_ablations/mlp_large_no_sig_ts/20261101-193234/README.md) | 4 | 0.9994 | 0.9992 | -0.0002 | 0.9946 | 0.9903 | -0.0043 | 0.9642 | 0.9068 | -0.0574 | 0.9950 | 0.9928 | -0.0023 | 0.0093 | 0.0096 | +0.0003 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1* pôvodný | F1* bez | Δ | FPR* pôvodný | FPR* bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_no_sig_ts](../../static_ablations/lightgbm_no_sig_ts/20261101-191319/README.md) | 4 | 0.9995 | 0.9994 | -0.0001 | 0.9943 | 0.9907 | -0.0036 | 0.9699 | 0.9659 | -0.0039 | 0.9900 | 0.9890 | -0.0010 | 0.0048 | 0.0049 | +0.0000 |
| [lr_no_sig_ts](../../static_ablations/lr_no_sig_ts/20261101-193217/README.md) | 4 | 0.9966 | 0.9958 | -0.0008 | 0.9667 | 0.9395 | -0.0272 | 0.0729 | 0.0114 | -0.0615 | 0.9694 | 0.9678 | -0.0016 | 0.0088 | 0.0107 | +0.0019 |
| [mlp_large_no_sig_ts](../../static_ablations/mlp_large_no_sig_ts/20261101-193234/README.md) | 4 | 0.9985 | 0.9977 | -0.0008 | 0.9835 | 0.9774 | -0.0061 | 0.8665 | 0.7915 | -0.0750 | 0.9861 | 0.9799 | -0.0063 | 0.0066 | 0.0069 | +0.0003 |
