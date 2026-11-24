# Kaskáda B `b_direct` – beh `20261123-221418`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T22:14:18+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/students_static/mlp_kd/20261123-221044` |
| hybrid | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/hybrid/lightgbm/20261123-220356` |

Druhý stupeň: **hybrid**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0067, hi = 0.9999, seed 1: lo = 0.0067, hi = 0.9994, seed 2: lo = 0.0101, hi = 0.9996).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9687 ± 0.0007 | 0.9658 ± 0.0009 | 0.9912 ± 0.0005 | 0.9384 ± 0.0021 | 0.0067 ± 0.0004 | 0.9641 ± 0.0009 | 0.9374 ± 0.0014 |
| statický | 0.9166 ± 0.0034 | 0.9077 ± 0.0038 | 0.9909 ± 0.0002 | 0.8214 ± 0.0076 | 0.0061 ± 0.0001 | 0.8982 ± 0.0046 | 0.8391 ± 0.0063 |
| hybrid (každá vzorka) | 0.9693 ± 0.0008 | 0.9665 ± 0.0009 | 0.9915 ± 0.0007 | 0.9395 ± 0.0023 | 0.0065 ± 0.0005 | 0.9648 ± 0.0009 | 0.9386 ± 0.0014 |

- **emulované súbory: 37.78%** (ostatné rozhodne iba statický model); na hybrid ide 37.78% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 145
- validácia: emulované 37.02%, na hybrid 37.02%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9774 ± 0.0003 | 0.9754 ± 0.0005 | 0.9865 ± 0.0006 | 0.9609 ± 0.0014 | 0.0100 ± 0.0005 | 0.9735 ± 0.0004 | 0.9540 ± 0.0007 |
| statický | 0.9295 ± 0.0075 | 0.9201 ± 0.0086 | 0.9852 ± 0.0003 | 0.8499 ± 0.0172 | 0.0097 ± 0.0000 | 0.9125 ± 0.0101 | 0.8606 ± 0.0141 |
| hybrid (každá vzorka) | 0.9778 ± 0.0005 | 0.9758 ± 0.0006 | 0.9872 ± 0.0002 | 0.9612 ± 0.0014 | 0.0096 ± 0.0002 | 0.9740 ± 0.0006 | 0.9549 ± 0.0010 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.3530 ± 0.0037 |
| statický | 0.1934 ± 0.0085 |
| hybrid (každá vzorka) | 0.3545 ± 0.0041 |

Podiel emulovaných: 37.95%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.0943 | 0.0943 | 0.8860 | 0.0034 | 0.9375 |
| 0.2000 | 0.2005 | 0.2005 | 0.9153 | 0.0053 | 0.9525 |
| 0.3000 | 0.2996 | 0.2996 | 0.9277 | 0.0060 | 0.9588 |
| 0.4000 | 0.3996 | 0.3996 | 0.9339 | 0.0063 | 0.9620 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **37.78%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
