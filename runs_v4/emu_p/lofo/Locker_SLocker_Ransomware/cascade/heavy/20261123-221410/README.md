# Kaskáda `heavy` – beh `20261123-221410`

> Generované `src/cascade/evaluate.py` (2026-11-23T22:14:10+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy sú určené na validácii (FPR ≤ 1 %); test sa na nič nenastavuje.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/students_static/mlp_kd/20261123-221044` |
| dynamic | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/students_dynamic/mlp_kd/20261123-221205` |
| hybrid | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/hybrid/mlp_large/20261123-220507` |

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9328 ± 0.0026 | 0.9254 ± 0.0029 | 0.9960 ± 0.0005 | 0.8536 ± 0.0055 | 0.0028 ± 0.0003 | 0.9193 ± 0.0034 | 0.8699 ± 0.0049 |
| hybrid (každá vzorka) | 0.9604 ± 0.0015 | 0.9567 ± 0.0016 | 0.9901 ± 0.0008 | 0.9209 ± 0.0025 | 0.0074 ± 0.0006 | 0.9543 ± 0.0017 | 0.9214 ± 0.0029 |
| statický | 0.9166 ± 0.0034 | 0.9077 ± 0.0038 | 0.9909 ± 0.0002 | 0.8214 ± 0.0076 | 0.0061 ± 0.0001 | 0.8982 ± 0.0046 | 0.8391 ± 0.0063 |
| dynamický | 0.8108 ± 0.0049 | 0.7898 ± 0.0056 | 0.9840 ± 0.0014 | 0.5875 ± 0.0117 | 0.0078 ± 0.0008 | 0.7356 ± 0.0089 | 0.6512 ± 0.0082 |
| neskorá fúzia (priemer) | 0.9255 ± 0.0031 | 0.9179 ± 0.0035 | 0.9878 ± 0.0008 | 0.8442 ± 0.0071 | 0.0085 ± 0.0006 | 0.9104 ± 0.0041 | 0.8549 ± 0.0057 |
| neskorá fúzia (stacking) | 0.9444 ± 0.0032 | 0.9388 ± 0.0038 | 0.9903 ± 0.0020 | 0.8846 ± 0.0091 | 0.0071 ± 0.0015 | 0.9344 ± 0.0042 | 0.8907 ± 0.0059 |

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda | 0.9476 ± 0.0034 | 0.9403 ± 0.0040 | 0.9920 ± 0.0012 | 0.8861 ± 0.0085 | 0.0054 ± 0.0009 | 0.9360 ± 0.0044 | 0.8960 ± 0.0064 |
| hybrid (každá vzorka) | 0.9704 ± 0.0012 | 0.9673 ± 0.0013 | 0.9867 ± 0.0000 | 0.9443 ± 0.0027 | 0.0097 ± 0.0000 | 0.9650 ± 0.0014 | 0.9400 ± 0.0023 |
| statický | 0.9295 ± 0.0075 | 0.9201 ± 0.0086 | 0.9852 ± 0.0003 | 0.8499 ± 0.0172 | 0.0097 ± 0.0000 | 0.9125 ± 0.0101 | 0.8606 ± 0.0141 |
| dynamický | 0.8278 ± 0.0073 | 0.8026 ± 0.0085 | 0.9797 ± 0.0005 | 0.6150 ± 0.0169 | 0.0097 ± 0.0000 | 0.7556 ± 0.0129 | 0.6741 ± 0.0132 |
| neskorá fúzia (priemer) | 0.9401 ± 0.0027 | 0.9324 ± 0.0031 | 0.9856 ± 0.0001 | 0.8745 ± 0.0062 | 0.0097 ± 0.0000 | 0.9268 ± 0.0035 | 0.8810 ± 0.0052 |
| neskorá fúzia (stacking) | 0.9566 ± 0.0033 | 0.9514 ± 0.0038 | 0.9862 ± 0.0001 | 0.9124 ± 0.0075 | 0.0097 ± 0.0000 | 0.9479 ± 0.0041 | 0.9128 ± 0.0064 |

## Správanie kaskády (test, seed 0)
- podiel eskalácií na hybrid: **15.66%** (1982 vzoriek)
- chyby pri zhode študentov (kaskáda ich nemôže opraviť): **753**
  (7.055% zo zhôd; FP 0, FN 753)
- úspešnosť na eskalovaných vzorkách: hybrid 0.9520686175580222, statický 0.855196770938446,
  dynamický 0.144803229061554  → prínos hybridu pri nezhode

## Výpočtové nároky (odhad z benchmarkov komponentov)
_Chýba benchmark niektorého komponentu (`python -m src.evaluation.benchmark`)._

![prístupy](plots/approaches_test.png)
![eskalácie](plots/escalation_by_family.png)
