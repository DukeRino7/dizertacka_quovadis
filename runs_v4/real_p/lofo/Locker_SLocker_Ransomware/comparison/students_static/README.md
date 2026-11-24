# Porovnanie modelov – students_static

> Generované `src/evaluation/compare.py` (2026-11-23T19:03:00+01:00); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu (meranie hneď po tréningu,
> orientačné). Oficiálne merania spotreby sú v časti „Spotreba zdrojov pri inferencii“.

## Detekčná kvalita a orientačné časy
| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [mlp_kd](../../students_static/mlp_kd/20261123-190146/README.md) | 0.9865 | 0.9779 ± 0.0018 | 0.8639 | 0.6225 | 0.8944 | 0.0059 | 0.0042 | 0.057 | 3 877 689 | 0.274 | 10 689 | 0.05 | 4.5 | 0.0 |
| [mlp_kd_heavy](../../students_static/mlp_kd_heavy/20261123-190246/README.md) | 0.9875 | 0.9798 ± 0.0007 | 0.8716 | 0.6335 | 0.9088 | 0.0064 | 0.0058 | 0.171 | 4 322 404 | 0.458 | 10 689 | 0.05 | 3.8 | 0.0 |
| [mlp_kd_modal](../../students_static/mlp_kd_modal/20261123-190224/README.md) | 0.9876 | 0.9798 ± 0.0014 | 0.8629 | 0.6838 | 0.9007 | 0.0065 | 0.0043 | 0.169 | 5 494 248 | 0.269 | 10 689 | 0.05 | 6.8 | 0.0 |
| [mlp_nokd](../../students_static/mlp_nokd/20261123-190201/README.md) | 0.9875 | 0.9790 ± 0.0006 | 0.8772 | 0.6169 | 0.9097 | 0.0060 | 0.0071 | 0.170 | 3 928 361 | 0.457 | 10 689 | 0.05 | 7.1 | 0.0 |

## Nízka prevalencia malvéru (test, prah z validácie)
| model | TPR | FPR | precision @ 1 % | falošné na 1 skutočný poplach @ 1 % | precision @ 0.1 % | falošné na 1 skutočný poplach @ 0.1 % |
|---|---|---|---|---|---|---|
| mlp_kd | 0.8149 | 0.0059 | 0.582 | 0.72 | 0.121 | 7.26 |
| mlp_kd_heavy | 0.8395 | 0.0064 | 0.568 | 0.76 | 0.115 | 7.67 |
| mlp_kd_modal | 0.8260 | 0.0065 | 0.561 | 0.78 | 0.112 | 7.91 |
| mlp_nokd | 0.8405 | 0.0060 | 0.587 | 0.70 | 0.124 | 7.09 |

Prepočet: TPR a FPR nezávisia od podielu malvéru, preto sa dajú preniesť na nízku prevalenciu (v reálnej prevádzke je malvéru ~1 % alebo menej; v teste 54 %). „Falošné na 1 skutočný poplach“ = koľko neškodných súborov je označených na každý zachytený malvér.

## Spotreba zdrojov pri inferencii (benchmark, testovacia množina)
_Benchmark zatiaľ nebol spustený (`python -m src.evaluation.benchmark --approach students_static`)._

## Grafy

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
