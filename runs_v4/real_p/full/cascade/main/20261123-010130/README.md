# Kaskáda `main` – beh `20261123-010130`

> Generované `src/cascade/evaluate.py` (2026-11-23T01:01:31+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/real_p/full/students_static/mlp_kd/20261123-002115` |
| dynamic | `runs_v4/real_p/full/students_dynamic/mlp_kd/20261123-003616` |
| hybrid | `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9634 ± 0.0011 | 0.9594 ± 0.0012 | 0.9976 ± 0.0003 | 0.9206 ± 0.0023 | 0.0018 ± 0.0002 | 0.9575 ± 0.0013 | 0.9278 ± 0.0021 |
| hybrid (každá vzorka) | 0.9835 ± 0.0003 | 0.9824 ± 0.0004 | 0.9922 ± 0.0004 | 0.9709 ± 0.0006 | 0.0062 ± 0.0003 | 0.9814 ± 0.0004 | 0.9668 ± 0.0007 |
| statický | 0.9236 ± 0.0011 | 0.9155 ± 0.0011 | 0.9909 ± 0.0015 | 0.8372 ± 0.0019 | 0.0063 ± 0.0011 | 0.9076 ± 0.0014 | 0.8520 ± 0.0022 |
| dynamický | 0.8717 ± 0.0041 | 0.8579 ± 0.0045 | 0.9857 ± 0.0014 | 0.7242 ± 0.0087 | 0.0085 ± 0.0008 | 0.8350 ± 0.0061 | 0.7573 ± 0.0075 |
| neskorá fúzia (priemer) | 0.9543 ± 0.0042 | 0.9498 ± 0.0048 | 0.9910 ± 0.0009 | 0.9063 ± 0.0101 | 0.0067 ± 0.0007 | 0.9467 ± 0.0052 | 0.9097 ± 0.0080 |
| neskorá fúzia (stacking) | 0.9688 ± 0.0006 | 0.9659 ± 0.0006 | 0.9919 ± 0.0007 | 0.9381 ± 0.0013 | 0.0062 ± 0.0006 | 0.9642 ± 0.0007 | 0.9378 ± 0.0012 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9610 ± 0.0004 | 0.9569 ± 0.0004 | 0.9953 ± 0.0006 | 0.9173 ± 0.0007 | 0.0035 ± 0.0004 | 0.9547 ± 0.0005 | 0.9229 ± 0.0008 |
| hybrid (každá vzorka) | 0.9816 ± 0.0004 | 0.9805 ± 0.0004 | 0.9879 ± 0.0002 | 0.9707 ± 0.0007 | 0.0096 ± 0.0002 | 0.9792 ± 0.0005 | 0.9628 ± 0.0008 |
| statický | 0.9157 ± 0.0003 | 0.9071 ± 0.0003 | 0.9857 ± 0.0000 | 0.8240 ± 0.0006 | 0.0097 ± 0.0000 | 0.8976 ± 0.0004 | 0.8365 ± 0.0005 |
| dynamický | 0.8711 ± 0.0035 | 0.8574 ± 0.0039 | 0.9839 ± 0.0004 | 0.7244 ± 0.0076 | 0.0096 ± 0.0002 | 0.8344 ± 0.0052 | 0.7559 ± 0.0062 |
| neskorá fúzia (priemer) | 0.9498 ± 0.0048 | 0.9452 ± 0.0054 | 0.9868 ± 0.0002 | 0.9001 ± 0.0108 | 0.0097 ± 0.0000 | 0.9414 ± 0.0060 | 0.9006 ± 0.0093 |
| neskorá fúzia (stacking) | 0.9652 ± 0.0008 | 0.9623 ± 0.0009 | 0.9873 ± 0.0000 | 0.9344 ± 0.0019 | 0.0097 ± 0.0000 | 0.9601 ± 0.0010 | 0.9304 ± 0.0016 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **13.57%** (1717 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **413**
  (3.775% zo zhôd; FP 0, FN 413)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9732090856144437, statický 0.675596971461852,
  dynamický 0.32440302853814795  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
| meranie | statický | dynamický | hybrid na každej vzorke | neskorá fúzia | kaskáda (odhad) |
|---|---|---|---|---|---|
| CPU čas ms/vz. (dávka) | 0.0352 | 0.0323 | 0.0575 | 0.0674 | 0.0754 |
| CPU čas ms/vz. (1 vz.) | 0.1375 | 0.1310 | 0.0496 | 0.2685 | 0.2754 |
| latencia ms (1 vz., postupne) | 0.0764 | 0.0762 | 0.0496 | 0.1526 | 0.1595 |

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
