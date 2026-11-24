# Porovnanie modelov – students_static

> Generované `src/evaluation/compare.py` (2026-11-23T22:27:30+01:00); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu (meranie hneď po tréningu,
> orientačné). Oficiálne merania spotreby sú v časti „Spotreba zdrojov pri inferencii“.

## Detekčná kvalita a orientačné časy
| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [mlp_kd](../../students_static/mlp_kd/20261123-222615/README.md) | 0.9871 | 0.9887 ± 0.0009 | 0.8860 | 0.6170 | 0.9199 | 0.0067 | 0.0053 | 0.061 | 4 444 600 | 0.291 | 10 625 | 0.05 | 4.8 | 0.0 |
| [mlp_kd_heavy](../../students_static/mlp_kd_heavy/20261123-222720/README.md) | 0.9850 | 0.9881 ± 0.0002 | 0.8815 | 0.6399 | 0.9127 | 0.0066 | 0.0065 | 0.168 | 4 507 283 | 0.444 | 10 625 | 0.05 | 2.9 | 0.0 |
| [mlp_kd_modal](../../students_static/mlp_kd_modal/20261123-222656/README.md) | 0.9874 | 0.9892 ± 0.0001 | 0.8914 | 0.6913 | 0.9176 | 0.0066 | 0.0046 | 0.168 | 6 465 720 | 0.267 | 10 625 | 0.05 | 7.2 | 0.0 |
| [mlp_nokd](../../students_static/mlp_nokd/20261123-222631/README.md) | 0.9871 | 0.9888 ± 0.0008 | 0.8818 | 0.5372 | 0.9203 | 0.0078 | 0.0066 | 0.167 | 5 496 395 | 0.439 | 10 625 | 0.05 | 7.8 | 0.0 |

## Nízka prevalencia malvéru (test, prah z validácie)
| model | TPR | FPR | precision @ 1 % | falošné na 1 skutočný poplach @ 1 % | precision @ 0.1 % | falošné na 1 skutočný poplach @ 0.1 % |
|---|---|---|---|---|---|---|
| mlp_kd | 0.8587 | 0.0067 | 0.563 | 0.78 | 0.113 | 7.83 |
| mlp_kd_heavy | 0.8462 | 0.0066 | 0.565 | 0.77 | 0.114 | 7.78 |
| mlp_kd_modal | 0.8546 | 0.0066 | 0.565 | 0.77 | 0.114 | 7.76 |
| mlp_nokd | 0.8606 | 0.0078 | 0.526 | 0.90 | 0.099 | 9.09 |

Prepočet: TPR a FPR nezávisia od podielu malvéru, preto sa dajú preniesť na nízku prevalenciu (v reálnej prevádzke je malvéru ~1 % alebo menej; v teste 54 %). „Falošné na 1 skutočný poplach“ = koľko neškodných súborov je označených na každý zachytený malvér.

## Spotreba zdrojov pri inferencii (benchmark, testovacia množina)
_Benchmark zatiaľ nebol spustený (`python -m src.evaluation.benchmark --approach students_static`)._

## Grafy

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
