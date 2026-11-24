# Porovnanie modelov – students_static

> Generované `src/evaluation/compare.py` (2026-11-23T18:51:04+01:00); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu (meranie hneď po tréningu,
> orientačné). Oficiálne merania spotreby sú v časti „Spotreba zdrojov pri inferencii“.

## Detekčná kvalita a orientačné časy
| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [mlp_kd](../../students_static/mlp_kd/20261123-184951/README.md) | 0.9866 | 0.9879 ± 0.0006 | 0.8777 | 0.6678 | 0.9118 | 0.0071 | 0.0037 | 0.060 | 4 139 871 | 0.263 | 10 689 | 0.05 | 4.8 | 0.0 |
| [mlp_kd_heavy](../../students_static/mlp_kd_heavy/20261123-185053/README.md) | 0.9867 | 0.9884 ± 0.0003 | 0.8820 | 0.6029 | 0.9145 | 0.0063 | 0.0053 | 0.169 | 4 271 491 | 0.473 | 10 689 | 0.05 | 3.1 | 0.0 |
| [mlp_kd_modal](../../students_static/mlp_kd_modal/20261123-185031/README.md) | 0.9870 | 0.9887 ± 0.0007 | 0.8885 | 0.6875 | 0.9193 | 0.0067 | 0.0043 | 0.170 | 4 193 923 | 0.461 | 10 689 | 0.05 | 6.8 | 0.0 |
| [mlp_nokd](../../students_static/mlp_nokd/20261123-185007/README.md) | 0.9870 | 0.9885 ± 0.0005 | 0.8827 | 0.5650 | 0.9136 | 0.0064 | 0.0064 | 0.170 | 3 954 876 | 0.475 | 10 689 | 0.05 | 7.4 | 0.0 |

## Nízka prevalencia malvéru (test, prah z validácie)
| model | TPR | FPR | precision @ 1 % | falošné na 1 skutočný poplach @ 1 % | precision @ 0.1 % | falošné na 1 skutočný poplach @ 0.1 % |
|---|---|---|---|---|---|---|
| mlp_kd | 0.8452 | 0.0071 | 0.546 | 0.83 | 0.106 | 8.41 |
| mlp_kd_heavy | 0.8489 | 0.0063 | 0.576 | 0.73 | 0.119 | 7.41 |
| mlp_kd_modal | 0.8577 | 0.0067 | 0.563 | 0.78 | 0.113 | 7.84 |
| mlp_nokd | 0.8476 | 0.0064 | 0.572 | 0.75 | 0.117 | 7.54 |

Prepočet: TPR a FPR nezávisia od podielu malvéru, preto sa dajú preniesť na nízku prevalenciu (v reálnej prevádzke je malvéru ~1 % alebo menej; v teste 54 %). „Falošné na 1 skutočný poplach“ = koľko neškodných súborov je označených na každý zachytený malvér.

## Spotreba zdrojov pri inferencii (benchmark, testovacia množina)
_Benchmark zatiaľ nebol spustený (`python -m src.evaluation.benchmark --approach students_static`)._

## Grafy

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
