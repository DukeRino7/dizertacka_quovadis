# Kaskáda `main` – beh `20261104-012447`

> Generované `src/cascade/evaluate.py` (2026-11-04T01:24:47+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v2/lofo/coinminer/students_static/mlp_kd/20261104-012050` |
| dynamic | `runs_v2/lofo/coinminer/students_dynamic/mlp_kd/20261104-012249` |
| hybrid | `runs_v2/lofo/coinminer/hybrid/lightgbm/20261104-001521` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9455 ± 0.0018 | 0.9495 ± 0.0017 | 0.9973 ± 0.0006 | 0.9019 ± 0.0028 | 0.0029 ± 0.0006 | 0.9472 ± 0.0018 | 0.8960 ± 0.0033 |
| hybrid (každá vzorka) | 0.9528 ± 0.0018 | 0.9560 ± 0.0016 | 0.9950 ± 0.0011 | 0.9175 ± 0.0043 | 0.0055 ± 0.0013 | 0.9547 ± 0.0018 | 0.9088 ± 0.0031 |
| statický | 0.9433 ± 0.0022 | 0.9472 ± 0.0021 | 0.9936 ± 0.0003 | 0.9012 ± 0.0039 | 0.0068 ± 0.0003 | 0.9452 ± 0.0023 | 0.8913 ± 0.0041 |
| dynamický | 0.7299 ± 0.0053 | 0.7499 ± 0.0047 | 0.9802 ± 0.0037 | 0.5121 ± 0.0120 | 0.0123 ± 0.0027 | 0.6727 ± 0.0095 | 0.5527 ± 0.0058 |
| neskorá fúzia (priemer) | 0.9335 ± 0.0035 | 0.9380 ± 0.0034 | 0.9918 ± 0.0019 | 0.8847 ± 0.0054 | 0.0086 ± 0.0020 | 0.9352 ± 0.0036 | 0.8734 ± 0.0066 |
| neskorá fúzia (stacking) | 0.9302 ± 0.0050 | 0.9352 ± 0.0046 | 0.9939 ± 0.0004 | 0.8767 ± 0.0093 | 0.0064 ± 0.0004 | 0.9316 ± 0.0053 | 0.8681 ± 0.0089 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9927 ± 0.0017 | 0.9932 ± 0.0016 | 0.9971 ± 0.0005 | 0.9914 ± 0.0023 | 0.0051 ± 0.0009 | 0.9942 ± 0.0014 | 0.9842 ± 0.0038 |
| hybrid (každá vzorka) | 0.9949 ± 0.0004 | 0.9940 ± 0.0004 | 0.9947 ± 0.0004 | 0.9974 ± 0.0004 | 0.0094 ± 0.0007 | 0.9960 ± 0.0003 | 0.9890 ± 0.0008 |
| statický | 0.9905 ± 0.0015 | 0.9905 ± 0.0011 | 0.9946 ± 0.0003 | 0.9905 ± 0.0024 | 0.0096 ± 0.0005 | 0.9926 ± 0.0012 | 0.9795 ± 0.0031 |
| dynamický | 0.9671 ± 0.0001 | 0.9721 ± 0.0001 | 0.9942 ± 0.0000 | 0.9540 ± 0.0002 | 0.0098 ± 0.0000 | 0.9737 ± 0.0001 | 0.9311 ± 0.0003 |
| neskorá fúzia (priemer) | 0.9931 ± 0.0004 | 0.9924 ± 0.0003 | 0.9945 ± 0.0000 | 0.9947 ± 0.0007 | 0.0098 ± 0.0000 | 0.9946 ± 0.0003 | 0.9849 ± 0.0010 |
| neskorá fúzia (stacking) | 0.9936 ± 0.0003 | 0.9930 ± 0.0003 | 0.9948 ± 0.0003 | 0.9953 ± 0.0005 | 0.0093 ± 0.0006 | 0.9950 ± 0.0002 | 0.9862 ± 0.0006 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **22.82%** (3957 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **859**
  (6.419% zo zhôd; FP 2, FN 857)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9871114480667172, statický 0.9800353803386403,
  dynamický 0.019964619661359616  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
