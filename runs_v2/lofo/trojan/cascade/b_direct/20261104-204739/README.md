# Kaskáda B `b_direct` – beh `20261104-204739`

> Generované `src/cascade/evaluate_b.py` (2026-11-04T20:47:39+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v2/lofo/trojan/students_static/mlp_kd/20261104-204353` |
| hybrid | `runs_v2/lofo/trojan/hybrid/lightgbm/20261104-193036` |

Druhý stupeň: **hybrid**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.5704, hi = 0.9982, seed 1: lo = 0.5120, hi = 0.9991, seed 2: lo = 0.5977, hi = 0.9984).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9714 ± 0.0014 | 0.9734 ± 0.0013 | 0.9979 ± 0.0002 | 0.9492 ± 0.0028 | 0.0024 ± 0.0003 | 0.9730 ± 0.0014 | 0.9440 ± 0.0027 |
| statický | 0.9645 ± 0.0045 | 0.9669 ± 0.0042 | 0.9956 ± 0.0001 | 0.9387 ± 0.0082 | 0.0049 ± 0.0001 | 0.9663 ± 0.0044 | 0.9307 ± 0.0084 |
| hybrid (každá vzorka) | 0.9819 ± 0.0015 | 0.9830 ± 0.0013 | 0.9964 ± 0.0007 | 0.9702 ± 0.0032 | 0.0042 ± 0.0008 | 0.9831 ± 0.0014 | 0.9641 ± 0.0028 |

- **emulované súbory: 12.88%** (ostatné rozhodne iba statický model); na hybrid ide 12.88% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 431
- validácia: emulované 4.12%, na hybrid 4.12%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9912 ± 0.0004 | 0.9918 ± 0.0005 | 0.9966 ± 0.0005 | 0.9894 ± 0.0004 | 0.0057 ± 0.0008 | 0.9930 ± 0.0004 | 0.9813 ± 0.0009 |
| statický | 0.9887 ± 0.0008 | 0.9892 ± 0.0005 | 0.9946 ± 0.0005 | 0.9873 ± 0.0018 | 0.0090 ± 0.0008 | 0.9910 ± 0.0007 | 0.9760 ± 0.0018 |
| hybrid (každá vzorka) | 0.9940 ± 0.0002 | 0.9934 ± 0.0003 | 0.9946 ± 0.0007 | 0.9959 ± 0.0007 | 0.0091 ± 0.0012 | 0.9952 ± 0.0002 | 0.9872 ± 0.0005 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.8838 ± 0.0200 |
| statický | 0.8610 ± 0.0122 |
| hybrid (každá vzorka) | 0.9318 ± 0.0090 |

Podiel emulovaných: 36.91%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.2294 | 0.2294 | 0.9718 | 0.0047 | 0.9837 |
| 0.2000 | 0.3660 | 0.3660 | 0.9703 | 0.0047 | 0.9830 |
| 0.3000 | 0.4896 | 0.4896 | 0.9703 | 0.0047 | 0.9830 |
| 0.4000 | 0.5462 | 0.5462 | 0.9703 | 0.0046 | 0.9830 |

## Výpočtové nároky
Emulácia (Speakeasy) sa nedá zmerať (dataset neobsahuje PE súbory). **Predpoklad** 60 s na súbor
(limit z `speakeasy-config.json`): kaskáda B ≈ 7.7 s na súbor v priemere, dynamický/hybridný model
a kaskáda A 60 s (emulujú každý súbor).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
