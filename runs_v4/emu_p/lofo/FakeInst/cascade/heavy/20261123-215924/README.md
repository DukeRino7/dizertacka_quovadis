# Kaskáda `heavy` – beh `20261123-215924`

> Generované `src/cascade/evaluate.py` (2026-11-23T21:59:24+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/FakeInst/students_static/mlp_kd/20261123-215606` |
| dynamic | `runs_v4/emu_p/lofo/FakeInst/students_dynamic/mlp_kd/20261123-215727` |
| hybrid | `runs_v4/emu_p/lofo/FakeInst/hybrid/mlp_large/20261123-215031` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9444 ± 0.0015 | 0.9383 ± 0.0017 | 0.9955 ± 0.0003 | 0.8798 ± 0.0033 | 0.0032 ± 0.0002 | 0.9341 ± 0.0019 | 0.8914 ± 0.0029 |
| hybrid (každá vzorka) | 0.9682 ± 0.0007 | 0.9654 ± 0.0008 | 0.9907 ± 0.0005 | 0.9379 ± 0.0019 | 0.0072 ± 0.0004 | 0.9636 ± 0.0009 | 0.9365 ± 0.0014 |
| statický | 0.9317 ± 0.0021 | 0.9246 ± 0.0024 | 0.9902 ± 0.0014 | 0.8561 ± 0.0058 | 0.0069 ± 0.0010 | 0.9183 ± 0.0028 | 0.8669 ± 0.0036 |
| dynamický | 0.8075 ± 0.0046 | 0.7862 ± 0.0052 | 0.9841 ± 0.0013 | 0.5799 ± 0.0110 | 0.0076 ± 0.0007 | 0.7297 ± 0.0085 | 0.6456 ± 0.0076 |
| neskorá fúzia (priemer) | 0.9260 ± 0.0067 | 0.9184 ± 0.0076 | 0.9888 ± 0.0025 | 0.8446 ± 0.0172 | 0.0078 ± 0.0019 | 0.9109 ± 0.0090 | 0.8561 ± 0.0119 |
| neskorá fúzia (stacking) | 0.9518 ± 0.0032 | 0.9471 ± 0.0037 | 0.9898 ± 0.0027 | 0.9018 ± 0.0095 | 0.0075 ± 0.0021 | 0.9437 ± 0.0040 | 0.9048 ± 0.0057 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9500 ± 0.0026 | 0.9426 ± 0.0029 | 0.9921 ± 0.0011 | 0.8906 ± 0.0053 | 0.0054 ± 0.0007 | 0.9386 ± 0.0033 | 0.9003 ± 0.0050 |
| hybrid (každá vzorka) | 0.9710 ± 0.0012 | 0.9678 ± 0.0014 | 0.9865 ± 0.0000 | 0.9454 ± 0.0027 | 0.0097 ± 0.0000 | 0.9655 ± 0.0014 | 0.9411 ± 0.0023 |
| statický | 0.9353 ± 0.0027 | 0.9262 ± 0.0031 | 0.9852 ± 0.0001 | 0.8621 ± 0.0063 | 0.0097 ± 0.0000 | 0.9195 ± 0.0036 | 0.8712 ± 0.0052 |
| dynamický | 0.8325 ± 0.0071 | 0.8065 ± 0.0083 | 0.9796 ± 0.0005 | 0.6227 ± 0.0166 | 0.0097 ± 0.0000 | 0.7613 ± 0.0126 | 0.6812 ± 0.0129 |
| neskorá fúzia (priemer) | 0.9429 ± 0.0046 | 0.9351 ± 0.0053 | 0.9855 ± 0.0002 | 0.8799 ± 0.0107 | 0.0097 ± 0.0000 | 0.9297 ± 0.0060 | 0.8859 ± 0.0089 |
| neskorá fúzia (stacking) | 0.9564 ± 0.0044 | 0.9508 ± 0.0052 | 0.9860 ± 0.0002 | 0.9114 ± 0.0103 | 0.0097 ± 0.0000 | 0.9472 ± 0.0057 | 0.9123 ± 0.0087 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **16.72%** (2116 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **624**
  (5.920% zo zhôd; FP 1, FN 623)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9560491493383743, statický 0.8879962192816635,
  dynamický 0.11200378071833648  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
