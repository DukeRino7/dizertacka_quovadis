# Porovnanie modelov – students_static

> Generované `src/evaluation/compare.py` (2026-11-23T21:26:41+01:00); použitý je posledný beh každého modelu.
> Metriky sú priemer cez seedy. \* = pri prahu určenom na validácii (FPR ≤ 1 %).
> CPU ms/vz. = medián latencie jednej vzorky na 1 vlákne vrátane transformácie vstupu (meranie hneď po tréningu,
> orientačné). Oficiálne merania spotreby sú v časti „Spotreba zdrojov pri inferencii“.

## Detekčná kvalita a orientačné časy
| model | ROC-AUC val | ROC-AUC test | TPR@FPR 1 % test | TPR@FPR 0,1 % test | F1 test* | FPR test* | gap train−val | CPU ms/vz. | CPU vz./s | GPU ms/vz. | parametre | MB | tréning s | ladenie min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [mlp_kd](../../students_static/mlp_kd/20261123-212524/README.md) | 0.9888 | 0.9780 ± 0.0008 | 0.7846 | 0.5802 | 0.8631 | 0.0086 | 0.0053 | 0.157 | 4 224 440 | 0.441 | 10 689 | 0.05 | 4.1 | 0.0 |
| [mlp_kd_heavy](../../students_static/mlp_kd_heavy/20261123-212630/README.md) | 0.9873 | 0.9759 ± 0.0008 | 0.7847 | 0.5742 | 0.8613 | 0.0086 | 0.0058 | 0.167 | 5 037 214 | 0.446 | 10 689 | 0.05 | 3.1 | 0.0 |
| [mlp_kd_modal](../../students_static/mlp_kd_modal/20261123-212605/README.md) | 0.9886 | 0.9771 ± 0.0008 | 0.7791 | 0.6282 | 0.8624 | 0.0090 | 0.0049 | 0.168 | 5 411 322 | 0.466 | 10 689 | 0.05 | 7.8 | 0.0 |
| [mlp_nokd](../../students_static/mlp_nokd/20261123-212539/README.md) | 0.9896 | 0.9770 ± 0.0012 | 0.7901 | 0.4918 | 0.8683 | 0.0090 | 0.0064 | 0.171 | 6 150 258 | 0.288 | 10 689 | 0.05 | 8.3 | 0.0 |

## Nízka prevalencia malvéru (test, prah z validácie)
| model | TPR | FPR | precision @ 1 % | falošné na 1 skutočný poplach @ 1 % | precision @ 0.1 % | falošné na 1 skutočný poplach @ 0.1 % |
|---|---|---|---|---|---|---|
| mlp_kd | 0.7672 | 0.0086 | 0.473 | 1.11 | 0.082 | 11.25 |
| mlp_kd_heavy | 0.7644 | 0.0086 | 0.473 | 1.11 | 0.082 | 11.23 |
| mlp_kd_modal | 0.7664 | 0.0090 | 0.463 | 1.16 | 0.079 | 11.70 |
| mlp_nokd | 0.7760 | 0.0090 | 0.466 | 1.14 | 0.080 | 11.55 |

Prepočet: TPR a FPR nezávisia od podielu malvéru, preto sa dajú preniesť na nízku prevalenciu (v reálnej prevádzke je malvéru ~1 % alebo menej; v teste 54 %). „Falošné na 1 skutočný poplach“ = koľko neškodných súborov je označených na každý zachytený malvér.

## Spotreba zdrojov pri inferencii (benchmark, testovacia množina)
_Benchmark zatiaľ nebol spustený (`python -m src.evaluation.benchmark --approach students_static`)._

## Grafy

![kvalita vs latencia](plots/auc_vs_latency.png)
![TPR vs latencia](plots/tpr1_vs_latency.png)
![ROC-AUC](plots/auc_test.png)
![TPR](plots/tpr1_test.png)
