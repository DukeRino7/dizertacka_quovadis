# Kaskáda B `b_heavy` – beh `20261123-211319`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T21:13:19+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/full/students_static/mlp_kd/20261123-203204` |
| dynamic | `runs_v4/emu_p/full/students_dynamic/mlp_kd/20261123-204643` |
| hybrid | `runs_v4/emu_p/full/hybrid/mlp_large/20261123-200933` |

Druhý stupeň: **dynamic**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0071, hi = 0.9999, seed 1: lo = 0.0066, hi = 0.9998, seed 2: lo = 0.0073, hi = 0.9998).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9477 ± 0.0008 | 0.9419 ± 0.0008 | 0.9964 ± 0.0000 | 0.8864 ± 0.0017 | 0.0026 ± 0.0000 | 0.9382 ± 0.0009 | 0.8977 ± 0.0014 |
| statický | 0.9312 ± 0.0031 | 0.9240 ± 0.0034 | 0.9908 ± 0.0011 | 0.8544 ± 0.0060 | 0.0064 ± 0.0007 | 0.9176 ± 0.0039 | 0.8660 ± 0.0059 |
| dynamický | 0.8170 ± 0.0032 | 0.7968 ± 0.0035 | 0.9830 ± 0.0009 | 0.6020 ± 0.0066 | 0.0084 ± 0.0004 | 0.7467 ± 0.0053 | 0.6615 ± 0.0057 |
| hybrid (každá vzorka) | 0.9716 ± 0.0005 | 0.9691 ± 0.0005 | 0.9919 ± 0.0003 | 0.9445 ± 0.0011 | 0.0063 ± 0.0002 | 0.9676 ± 0.0006 | 0.9433 ± 0.0010 |

- **emulované súbory: 36.53%** (ostatné rozhodne iba statický model); na hybrid ide 9.33% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 59
- validácia: emulované 36.55%, na hybrid 9.91%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9459 ± 0.0009 | 0.9404 ± 0.0009 | 0.9913 ± 0.0010 | 0.8871 ± 0.0015 | 0.0063 ± 0.0008 | 0.9363 ± 0.0011 | 0.8937 ± 0.0018 |
| statický | 0.9279 ± 0.0046 | 0.9207 ± 0.0051 | 0.9861 ± 0.0002 | 0.8511 ± 0.0102 | 0.0097 ± 0.0000 | 0.9136 ± 0.0059 | 0.8592 ± 0.0086 |
| dynamický | 0.8204 ± 0.0031 | 0.8008 ± 0.0034 | 0.9808 ± 0.0002 | 0.6114 ± 0.0068 | 0.0097 ± 0.0000 | 0.7532 ± 0.0052 | 0.6668 ± 0.0053 |
| hybrid (každá vzorka) | 0.9690 ± 0.0007 | 0.9665 ± 0.0007 | 0.9874 ± 0.0000 | 0.9427 ± 0.0015 | 0.0097 ± 0.0000 | 0.9646 ± 0.0008 | 0.9378 ± 0.0013 |

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.0911 | 0.0421 | 0.8743 | 0.0028 | 0.9312 |
| 0.2000 | 0.1955 | 0.0743 | 0.8811 | 0.0024 | 0.9353 |
| 0.3000 | 0.2955 | 0.1028 | 0.8851 | 0.0024 | 0.9376 |
| 0.4000 | 0.3982 | 0.1219 | 0.8857 | 0.0025 | 0.9378 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **36.53%** (ostatné prístupy 100 %).

| meranie | statický | dynamický | hybrid na každej vzorke | kaskáda B (odhad) |
|---|---|---|---|---|
| CPU čas ms/vz. (dávka) | 0.0313 | 0.0332 | 0.1076 | 0.0535 |
| CPU čas ms/vz. (1 vz.) | 0.1131 | 0.1138 | 0.3154 | 0.1841 |

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
