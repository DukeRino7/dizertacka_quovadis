# Kaskáda B `b_baselines` – beh `20261123-191733`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T19:17:33+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/real_p/lofo/BankBot/static/lightgbm/20261123-190600` |
| dynamic | `runs_v4/real_p/lofo/BankBot/dynamic/lightgbm/20261123-190812` |
| hybrid | `runs_v4/real_p/lofo/BankBot/hybrid/lightgbm/20261123-191024` |

Druhý stupeň: **dynamic**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0025, hi = 0.9997, seed 1: lo = 0.0065, hi = 0.9988, seed 2: lo = 0.0028, hi = 0.9994).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9830 ± 0.0001 | 0.9815 ± 0.0001 | 0.9956 ± 0.0005 | 0.9664 ± 0.0004 | 0.0035 ± 0.0004 | 0.9808 ± 0.0001 | 0.9660 ± 0.0002 |
| statický | 0.9708 ± 0.0013 | 0.9683 ± 0.0015 | 0.9897 ± 0.0007 | 0.9447 ± 0.0033 | 0.0080 ± 0.0006 | 0.9667 ± 0.0016 | 0.9415 ± 0.0026 |
| dynamický | 0.9213 ± 0.0012 | 0.9130 ± 0.0014 | 0.9904 ± 0.0012 | 0.8325 ± 0.0032 | 0.0066 ± 0.0009 | 0.9046 ± 0.0017 | 0.8476 ± 0.0022 |
| hybrid (každá vzorka) | 0.9839 ± 0.0007 | 0.9828 ± 0.0008 | 0.9912 ± 0.0002 | 0.9726 ± 0.0017 | 0.0070 ± 0.0001 | 0.9818 ± 0.0008 | 0.9674 ± 0.0015 |

- **emulované súbory: 15.51%** (ostatné rozhodne iba statický model); na hybrid ide 3.69% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 52
- validácia: emulované 15.15%, na hybrid 3.33%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9804 ± 0.0002 | 0.9783 ± 0.0003 | 0.9934 ± 0.0004 | 0.9616 ± 0.0006 | 0.0050 ± 0.0003 | 0.9772 ± 0.0003 | 0.9605 ± 0.0005 |
| statický | 0.9699 ± 0.0018 | 0.9669 ± 0.0021 | 0.9870 ± 0.0002 | 0.9435 ± 0.0041 | 0.0096 ± 0.0002 | 0.9648 ± 0.0022 | 0.9392 ± 0.0036 |
| dynamický | 0.9217 ± 0.0023 | 0.9119 ± 0.0026 | 0.9853 ± 0.0003 | 0.8334 ± 0.0052 | 0.0096 ± 0.0002 | 0.9030 ± 0.0031 | 0.8465 ± 0.0043 |
| hybrid (každá vzorka) | 0.9815 ± 0.0007 | 0.9802 ± 0.0008 | 0.9876 ± 0.0000 | 0.9699 ± 0.0015 | 0.0095 ± 0.0000 | 0.9786 ± 0.0008 | 0.9625 ± 0.0014 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.9942 ± 0.0006 |
| statický | 0.9851 ± 0.0006 |
| dynamický | 0.7526 ± 0.0764 |
| hybrid (každá vzorka) | 0.9942 ± 0.0006 |

Podiel emulovaných: 8.56%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.1054 | 0.0346 | 0.9615 | 0.0032 | 0.9784 |
| 0.2000 | 0.2023 | 0.0498 | 0.9642 | 0.0034 | 0.9797 |
| 0.3000 | 0.3018 | 0.0585 | 0.9658 | 0.0035 | 0.9805 |
| 0.4000 | 0.4043 | 0.0671 | 0.9667 | 0.0035 | 0.9810 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **15.51%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
