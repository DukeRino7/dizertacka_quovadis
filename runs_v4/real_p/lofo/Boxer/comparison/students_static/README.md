# Porovnanie modelov – students_static

> Generované `src/evaluation/compare.py` (2026-11-23T18:39:23+01:00); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu (meranie hneď po tréningu,
> orientačné). Oficiálne merania spotreby sú v časti „Spotreba zdrojov pri inferencii“.

## Detekčná kvalita a orientačné časy
| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [mlp_kd](../../students_static/mlp_kd/20261123-183817/README.md) | 0.9858 | 0.9869 ± 0.0003 | 0.8414 | 0.5387 | 0.8660 | 0.0064 | 0.0037 | 0.076 | 3 859 596 | 0.290 | 10 689 | 0.05 | 3.8 | 0.0 |
| [mlp_kd_heavy](../../students_static/mlp_kd_heavy/20261123-183913/README.md) | 0.9857 | 0.9873 ± 0.0009 | 0.8750 | 0.5498 | 0.9045 | 0.0062 | 0.0061 | 0.170 | 4 750 216 | 0.476 | 10 689 | 0.05 | 2.7 | 0.0 |
| [mlp_kd_modal](../../students_static/mlp_kd_modal/20261123-183851/README.md) | 0.9864 | 0.9880 ± 0.0009 | 0.8807 | 0.5804 | 0.9131 | 0.0074 | 0.0046 | 0.169 | 5 715 834 | 0.282 | 10 689 | 0.05 | 6.9 | 0.0 |
| [mlp_nokd](../../students_static/mlp_nokd/20261123-183830/README.md) | 0.9860 | 0.9871 ± 0.0007 | 0.8732 | 0.5110 | 0.9024 | 0.0075 | 0.0072 | 0.170 | 3 854 189 | 0.453 | 10 689 | 0.05 | 6.3 | 0.0 |

## Nízka prevalencia malvéru (test, prah z validácie)
| model | TPR | FPR | precision @ 1 % | falošné na 1 skutočný poplach @ 1 % | precision @ 0.1 % | falošné na 1 skutočný poplach @ 0.1 % |
|---|---|---|---|---|---|---|
| mlp_kd | 0.7701 | 0.0064 | 0.547 | 0.83 | 0.107 | 8.36 |
| mlp_kd_heavy | 0.8320 | 0.0062 | 0.575 | 0.74 | 0.118 | 7.45 |
| mlp_kd_modal | 0.8477 | 0.0074 | 0.536 | 0.86 | 0.103 | 8.72 |
| mlp_nokd | 0.8299 | 0.0075 | 0.528 | 0.89 | 0.100 | 9.02 |

Prepočet: TPR a FPR nezávisia od podielu malvéru, preto sa dajú preniesť na nízku prevalenciu (v reálnej prevádzke je malvéru ~1 % alebo menej; v teste 54 %). „Falošné na 1 skutočný poplach“ = koľko neškodných súborov je označených na každý zachytený malvér.

## Spotreba zdrojov pri inferencii (benchmark, testovacia množina)
_Benchmark zatiaľ nebol spustený (`python -m src.evaluation.benchmark --approach students_static`)._

## Grafy

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
