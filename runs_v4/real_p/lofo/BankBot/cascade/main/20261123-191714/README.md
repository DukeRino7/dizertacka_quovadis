# Kaskáda `main` – beh `20261123-191714`

> Generované `src/cascade/evaluate.py` (2026-11-23T19:17:15+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/real_p/lofo/BankBot/students_static/mlp_kd/20261123-191350` |
| dynamic | `runs_v4/real_p/lofo/BankBot/students_dynamic/mlp_kd/20261123-191512` |
| hybrid | `runs_v4/real_p/lofo/BankBot/hybrid/lightgbm/20261123-191024` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9644 ± 0.0024 | 0.9606 ± 0.0027 | 0.9966 ± 0.0004 | 0.9238 ± 0.0054 | 0.0025 ± 0.0003 | 0.9588 ± 0.0029 | 0.9297 ± 0.0047 |
| hybrid (každá vzorka) | 0.9839 ± 0.0007 | 0.9828 ± 0.0008 | 0.9912 ± 0.0002 | 0.9726 ± 0.0017 | 0.0070 ± 0.0001 | 0.9818 ± 0.0008 | 0.9674 ± 0.0015 |
| statický | 0.9252 ± 0.0046 | 0.9173 ± 0.0052 | 0.9904 ± 0.0008 | 0.8412 ± 0.0110 | 0.0066 ± 0.0006 | 0.9097 ± 0.0062 | 0.8548 ± 0.0085 |
| dynamický | 0.8708 ± 0.0052 | 0.8570 ± 0.0059 | 0.9838 ± 0.0005 | 0.7237 ± 0.0122 | 0.0097 ± 0.0005 | 0.8339 ± 0.0080 | 0.7553 ± 0.0091 |
| neskorá fúzia (priemer) | 0.9544 ± 0.0019 | 0.9499 ± 0.0022 | 0.9908 ± 0.0006 | 0.9067 ± 0.0048 | 0.0068 ± 0.0005 | 0.9469 ± 0.0024 | 0.9098 ± 0.0037 |
| neskorá fúzia (stacking) | 0.9696 ± 0.0022 | 0.9668 ± 0.0025 | 0.9918 ± 0.0006 | 0.9399 ± 0.0053 | 0.0063 ± 0.0005 | 0.9652 ± 0.0026 | 0.9393 ± 0.0042 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9626 ± 0.0025 | 0.9576 ± 0.0028 | 0.9955 ± 0.0006 | 0.9185 ± 0.0053 | 0.0032 ± 0.0004 | 0.9555 ± 0.0031 | 0.9255 ± 0.0049 |
| hybrid (každá vzorka) | 0.9815 ± 0.0007 | 0.9802 ± 0.0008 | 0.9876 ± 0.0000 | 0.9699 ± 0.0015 | 0.0095 ± 0.0000 | 0.9786 ± 0.0008 | 0.9625 ± 0.0014 |
| statický | 0.9183 ± 0.0064 | 0.9079 ± 0.0073 | 0.9850 ± 0.0003 | 0.8256 ± 0.0146 | 0.0097 ± 0.0000 | 0.8983 ± 0.0087 | 0.8400 ± 0.0119 |
| dynamický | 0.8718 ± 0.0056 | 0.8547 ± 0.0064 | 0.9828 ± 0.0003 | 0.7192 ± 0.0127 | 0.0097 ± 0.0000 | 0.8306 ± 0.0086 | 0.7545 ± 0.0100 |
| neskorá fúzia (priemer) | 0.9503 ± 0.0033 | 0.9445 ± 0.0037 | 0.9862 ± 0.0001 | 0.8987 ± 0.0075 | 0.0097 ± 0.0000 | 0.9404 ± 0.0042 | 0.9008 ± 0.0063 |
| neskorá fúzia (stacking) | 0.9661 ± 0.0019 | 0.9626 ± 0.0022 | 0.9868 ± 0.0001 | 0.9349 ± 0.0043 | 0.0097 ± 0.0000 | 0.9601 ± 0.0023 | 0.9317 ± 0.0037 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **13.99%** (1771 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **400**
  (3.675% zo zhôd; FP 1, FN 399)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9700734048560136, statický 0.6804065499717674,
  dynamický 0.31959345002823264  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
