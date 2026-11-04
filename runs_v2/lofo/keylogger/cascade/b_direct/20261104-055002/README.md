# Kaskáda B `b_direct` – beh `20261104-055002`

> Generované `src/cascade/evaluate_b.py` (2026-11-04T05:50:03+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v2/lofo/keylogger/students_static/mlp_kd/20261104-054525` |
| hybrid | `runs_v2/lofo/keylogger/hybrid/lightgbm/20261104-043557` |

Druhý stupeň: **hybrid**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.9241, hi = 0.9960, seed 1: lo = 0.9304, hi = 0.9968, seed 2: lo = 0.9303, hi = 0.9978).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9105 ± 0.0040 | 0.9173 ± 0.0037 | 0.9980 ± 0.0004 | 0.8365 ± 0.0075 | 0.0020 ± 0.0004 | 0.9101 ± 0.0044 | 0.8351 ± 0.0068 |
| statický | 0.9364 ± 0.0059 | 0.9409 ± 0.0054 | 0.9945 ± 0.0006 | 0.8876 ± 0.0111 | 0.0058 ± 0.0007 | 0.9380 ± 0.0061 | 0.8792 ± 0.0104 |
| hybrid (každá vzorka) | 0.9318 ± 0.0015 | 0.9368 ± 0.0013 | 0.9963 ± 0.0006 | 0.8775 ± 0.0032 | 0.0038 ± 0.0007 | 0.9331 ± 0.0016 | 0.8714 ± 0.0024 |

- **emulované súbory: 6.24%** (ostatné rozhodne iba statický model); na hybrid ide 6.24% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 1415
- validácia: emulované 1.53%, na hybrid 1.53%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9929 ± 0.0002 | 0.9942 ± 0.0003 | 0.9990 ± 0.0003 | 0.9901 ± 0.0001 | 0.0018 ± 0.0005 | 0.9946 ± 0.0002 | 0.9846 ± 0.0005 |
| statický | 0.9929 ± 0.0001 | 0.9923 ± 0.0002 | 0.9949 ± 0.0001 | 0.9942 ± 0.0001 | 0.0096 ± 0.0002 | 0.9946 ± 0.0001 | 0.9843 ± 0.0003 |
| hybrid (každá vzorka) | 0.9954 ± 0.0004 | 0.9945 ± 0.0004 | 0.9955 ± 0.0003 | 0.9974 ± 0.0002 | 0.0085 ± 0.0006 | 0.9964 ± 0.0003 | 0.9897 ± 0.0008 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.3318 ± 0.0133 |
| statický | 0.4061 ± 0.0020 |
| hybrid (každá vzorka) | 0.3950 ± 0.0089 |

Podiel emulovaných: 8.35%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.2317 | 0.2317 | 0.8775 | 0.0045 | 0.9329 |
| 0.2000 | 0.3637 | 0.3637 | 0.8775 | 0.0042 | 0.9330 |
| 0.3000 | 0.4554 | 0.4554 | 0.8775 | 0.0042 | 0.9330 |
| 0.4000 | 0.5518 | 0.5518 | 0.8775 | 0.0041 | 0.9330 |

## Výpočtové nároky
Emulácia (Speakeasy) sa nedá zmerať (dataset neobsahuje PE súbory). **Predpoklad** 60 s na súbor
(limit z `speakeasy-config.json`): kaskáda B ≈ 3.7 s na súbor v priemere, dynamický/hybridný model
a kaskáda A 60 s (emulujú každý súbor).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
