# Kaskáda `main` – beh `20261122-212745`

> Generované `src/cascade/evaluate.py` (2026-11-22T21:27:45+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/real_full/full/students_static/mlp_kd/20261122-203423` |
| dynamic | `runs_v4/real_full/full/students_dynamic/mlp_kd/20261122-205301` |
| hybrid | `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9666 ± 0.0012 | 0.9683 ± 0.0011 | 0.9972 ± 0.0003 | 0.9397 ± 0.0022 | 0.0030 ± 0.0004 | 0.9676 ± 0.0012 | 0.9350 ± 0.0022 |
| hybrid (každá vzorka) | 0.9818 ± 0.0005 | 0.9824 ± 0.0005 | 0.9931 ± 0.0005 | 0.9724 ± 0.0006 | 0.0076 ± 0.0005 | 0.9826 ± 0.0005 | 0.9638 ± 0.0010 |
| statický | 0.9348 ± 0.0031 | 0.9380 ± 0.0029 | 0.9927 ± 0.0004 | 0.8834 ± 0.0063 | 0.0073 ± 0.0005 | 0.9348 ± 0.0034 | 0.8760 ± 0.0056 |
| dynamický | 0.8626 ± 0.0048 | 0.8697 ± 0.0045 | 0.9886 ± 0.0005 | 0.7492 ± 0.0095 | 0.0098 ± 0.0006 | 0.8524 ± 0.0060 | 0.7529 ± 0.0076 |
| neskorá fúzia (priemer) | 0.9447 ± 0.0053 | 0.9475 ± 0.0050 | 0.9942 ± 0.0009 | 0.9008 ± 0.0108 | 0.0059 ± 0.0010 | 0.9452 ± 0.0056 | 0.8941 ± 0.0095 |
| neskorá fúzia (stacking) | 0.9682 ± 0.0009 | 0.9696 ± 0.0008 | 0.9945 ± 0.0013 | 0.9452 ± 0.0024 | 0.0059 ± 0.0014 | 0.9692 ± 0.0009 | 0.9377 ± 0.0016 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9664 ± 0.0003 | 0.9680 ± 0.0003 | 0.9951 ± 0.0005 | 0.9411 ± 0.0010 | 0.0052 ± 0.0005 | 0.9674 ± 0.0003 | 0.9343 ± 0.0005 |
| hybrid (každá vzorka) | 0.9807 ± 0.0001 | 0.9812 ± 0.0001 | 0.9914 ± 0.0002 | 0.9720 ± 0.0005 | 0.0095 ± 0.0003 | 0.9816 ± 0.0001 | 0.9615 ± 0.0002 |
| statický | 0.9349 ± 0.0023 | 0.9380 ± 0.0022 | 0.9903 ± 0.0000 | 0.8857 ± 0.0044 | 0.0098 ± 0.0000 | 0.9351 ± 0.0025 | 0.8756 ± 0.0042 |
| dynamický | 0.8643 ± 0.0056 | 0.8713 ± 0.0053 | 0.9886 ± 0.0002 | 0.7524 ± 0.0105 | 0.0098 ± 0.0000 | 0.8545 ± 0.0069 | 0.7557 ± 0.0090 |
| neskorá fúzia (priemer) | 0.9396 ± 0.0054 | 0.9425 ± 0.0051 | 0.9904 ± 0.0001 | 0.8947 ± 0.0101 | 0.0098 ± 0.0000 | 0.9401 ± 0.0056 | 0.8842 ± 0.0097 |
| neskorá fúzia (stacking) | 0.9666 ± 0.0021 | 0.9680 ± 0.0020 | 0.9911 ± 0.0003 | 0.9456 ± 0.0037 | 0.0096 ± 0.0003 | 0.9678 ± 0.0021 | 0.9344 ± 0.0040 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **14.95%** (2336 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **462**
  (3.477% zo zhôd; FP 1, FN 461)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9721746575342466, statický 0.7564212328767124,
  dynamický 0.24357876712328766  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
| meranie | statický | dynamický | hybrid na každej vzorke | neskorá fúzia | kaskáda (odhad) |
|---|---|---|---|---|---|
| CPU čas ms/vz. (dávka) | 0.0476 | 0.0353 | 0.1787 | 0.0829 | 0.1089 |
| CPU čas ms/vz. (1 vz.) | 0.1442 | 0.1408 | 0.1223 | 0.2849 | 0.3027 |
| latencia ms (1 vz., postupne) | 0.0799 | 0.0790 | 0.1271 | 0.1589 | 0.1774 |

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
