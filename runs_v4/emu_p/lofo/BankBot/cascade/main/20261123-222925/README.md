# Kaskáda `main` – beh `20261123-222925`

> Generované `src/cascade/evaluate.py` (2026-11-23T22:29:25+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/BankBot/students_static/mlp_kd/20261123-222615` |
| dynamic | `runs_v4/emu_p/lofo/BankBot/students_dynamic/mlp_kd/20261123-222733` |
| hybrid | `runs_v4/emu_p/lofo/BankBot/hybrid/lightgbm/20261123-221915` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9515 ± 0.0008 | 0.9461 ± 0.0009 | 0.9969 ± 0.0001 | 0.8945 ± 0.0018 | 0.0022 ± 0.0001 | 0.9430 ± 0.0010 | 0.9050 ± 0.0016 |
| hybrid (každá vzorka) | 0.9788 ± 0.0009 | 0.9771 ± 0.0009 | 0.9916 ± 0.0005 | 0.9608 ± 0.0016 | 0.0066 ± 0.0004 | 0.9759 ± 0.0010 | 0.9573 ± 0.0017 |
| statický | 0.9330 ± 0.0016 | 0.9260 ± 0.0018 | 0.9904 ± 0.0009 | 0.8587 ± 0.0032 | 0.0067 ± 0.0006 | 0.9199 ± 0.0021 | 0.8693 ± 0.0031 |
| dynamický | 0.8148 ± 0.0040 | 0.7943 ± 0.0044 | 0.9832 ± 0.0026 | 0.5970 ± 0.0090 | 0.0083 ± 0.0013 | 0.7429 ± 0.0069 | 0.6578 ± 0.0069 |
| neskorá fúzia (priemer) | 0.9343 ± 0.0032 | 0.9277 ± 0.0037 | 0.9880 ± 0.0005 | 0.8640 ± 0.0078 | 0.0085 ± 0.0004 | 0.9218 ± 0.0042 | 0.8715 ± 0.0060 |
| neskorá fúzia (stacking) | 0.9545 ± 0.0024 | 0.9502 ± 0.0027 | 0.9891 ± 0.0009 | 0.9086 ± 0.0054 | 0.0082 ± 0.0007 | 0.9471 ± 0.0030 | 0.9099 ± 0.0047 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9494 ± 0.0009 | 0.9428 ± 0.0010 | 0.9934 ± 0.0004 | 0.8902 ± 0.0023 | 0.0046 ± 0.0003 | 0.9390 ± 0.0012 | 0.9000 ± 0.0017 |
| hybrid (každá vzorka) | 0.9759 ± 0.0005 | 0.9737 ± 0.0006 | 0.9874 ± 0.0004 | 0.9569 ± 0.0009 | 0.0095 ± 0.0003 | 0.9719 ± 0.0006 | 0.9511 ± 0.0010 |
| statický | 0.9283 ± 0.0008 | 0.9194 ± 0.0009 | 0.9856 ± 0.0002 | 0.8484 ± 0.0019 | 0.0096 ± 0.0002 | 0.9119 ± 0.0010 | 0.8588 ± 0.0014 |
| dynamický | 0.8178 ± 0.0054 | 0.7930 ± 0.0062 | 0.9794 ± 0.0004 | 0.5958 ± 0.0124 | 0.0097 ± 0.0000 | 0.7408 ± 0.0097 | 0.6580 ± 0.0097 |
| neskorá fúzia (priemer) | 0.9365 ± 0.0037 | 0.9288 ± 0.0042 | 0.9857 ± 0.0001 | 0.8674 ± 0.0084 | 0.0097 ± 0.0000 | 0.9228 ± 0.0048 | 0.8744 ± 0.0070 |
| neskorá fúzia (stacking) | 0.9534 ± 0.0035 | 0.9481 ± 0.0040 | 0.9867 ± 0.0003 | 0.9056 ± 0.0083 | 0.0095 ± 0.0003 | 0.9444 ± 0.0044 | 0.9070 ± 0.0067 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **16.55%** (2094 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **553**
  (5.236% zo zhôd; FP 1, FN 552)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9737344794651385, statický 0.8634192932187201,
  dynamický 0.13658070678127984  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
