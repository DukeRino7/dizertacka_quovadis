# Kontrolné experimenty – static_ablations

> Generované `src/evaluation/compare_ablations.py` (2026-11-02T00:20:23+01:00). Hyperparametre ablácie sú prevzaté z pôvodného
> behu, rozdiel teda spôsobujú iba vynechané príznaky. Hodnoty sú priemer cez seedy; (*) = prah z validácie (FPR ≤ 1 %).
> Δ < 0 = bez príznakov horšie (pri FPR naopak: Δ > 0 = viac falošných poplachov).

### validácia
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_no_sig_ts](../../static_ablations/lightgbm_no_sig_ts/20261102-000021/README.md) | 4 | 0.9998 | 0.9998 | -0.0001 | 0.9978 | 0.9966 | -0.0012 | 0.9900 | 0.9838 | -0.0062 | 0.9967 | 0.9962 | -0.0005 | 0.0089 | 0.0085 | -0.0004 |
| [lr_no_sig_ts](../../static_ablations/lr_no_sig_ts/20261102-001940/README.md) | 4 | 0.9986 | 0.9981 | -0.0005 | 0.9839 | 0.9801 | -0.0038 | 0.8270 | 0.8108 | -0.0163 | 0.9896 | 0.9876 | -0.0020 | 0.0094 | 0.0098 | +0.0004 |
| [mlp_large_no_sig_ts](../../static_ablations/mlp_large_no_sig_ts/20261102-001955/README.md) | 4 | 0.9995 | 0.9994 | -0.0002 | 0.9954 | 0.9930 | -0.0024 | 0.9773 | 0.9420 | -0.0353 | 0.9954 | 0.9942 | -0.0011 | 0.0096 | 0.0093 | -0.0003 |

### test
| ablácia | vynechaných | ROC-AUC pôvodný | ROC-AUC bez | Δ | TPR@FPR 1 % pôvodný | TPR@FPR 1 % bez | Δ | TPR@FPR 0,1 % pôvodný | TPR@FPR 0,1 % bez | Δ | F1 (*) pôvodný | F1 (*) bez | Δ | FPR (*) pôvodný | FPR (*) bez | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [lightgbm_no_sig_ts](../../static_ablations/lightgbm_no_sig_ts/20261102-000021/README.md) | 4 | 0.9995 | 0.9994 | -0.0001 | 0.9943 | 0.9907 | -0.0036 | 0.9699 | 0.9659 | -0.0039 | 0.9900 | 0.9890 | -0.0010 | 0.0048 | 0.0049 | +0.0000 |
| [lr_no_sig_ts](../../static_ablations/lr_no_sig_ts/20261102-001940/README.md) | 4 | 0.9966 | 0.9958 | -0.0007 | 0.9671 | 0.9423 | -0.0248 | 0.0788 | 0.0113 | -0.0676 | 0.9700 | 0.9680 | -0.0020 | 0.0088 | 0.0105 | +0.0016 |
| [mlp_large_no_sig_ts](../../static_ablations/mlp_large_no_sig_ts/20261102-001955/README.md) | 4 | 0.9986 | 0.9984 | -0.0002 | 0.9882 | 0.9791 | -0.0091 | 0.8693 | 0.8627 | -0.0066 | 0.9870 | 0.9801 | -0.0069 | 0.0065 | 0.0066 | +0.0001 |
