# Kaskáda B `b_heavy` – beh `20261123-221420`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T22:14:20+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/students_static/mlp_kd/20261123-221044` |
| dynamic | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/students_dynamic/mlp_kd/20261123-221205` |
| hybrid | `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/hybrid/mlp_large/20261123-220507` |

Druhý stupeň: **dynamic**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0067, hi = 0.9999, seed 1: lo = 0.0067, hi = 0.9994, seed 2: lo = 0.0101, hi = 0.9996).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9333 ± 0.0027 | 0.9259 ± 0.0030 | 0.9962 ± 0.0004 | 0.8545 ± 0.0057 | 0.0027 ± 0.0003 | 0.9199 ± 0.0035 | 0.8708 ± 0.0050 |
| statický | 0.9166 ± 0.0034 | 0.9077 ± 0.0038 | 0.9909 ± 0.0002 | 0.8214 ± 0.0076 | 0.0061 ± 0.0001 | 0.8982 ± 0.0046 | 0.8391 ± 0.0063 |
| dynamický | 0.8108 ± 0.0049 | 0.7898 ± 0.0056 | 0.9840 ± 0.0014 | 0.5875 ± 0.0117 | 0.0078 ± 0.0008 | 0.7356 ± 0.0089 | 0.6512 ± 0.0082 |
| hybrid (každá vzorka) | 0.9604 ± 0.0015 | 0.9567 ± 0.0016 | 0.9901 ± 0.0008 | 0.9209 ± 0.0025 | 0.0074 ± 0.0006 | 0.9543 ± 0.0017 | 0.9214 ± 0.0029 |

- **emulované súbory: 37.78%** (ostatné rozhodne iba statický model); na hybrid ide 8.99% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 145
- validácia: emulované 37.02%, na hybrid 9.42%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9473 ± 0.0033 | 0.9401 ± 0.0039 | 0.9913 ± 0.0012 | 0.8861 ± 0.0083 | 0.0059 ± 0.0009 | 0.9357 ± 0.0044 | 0.8954 ± 0.0064 |
| statický | 0.9295 ± 0.0075 | 0.9201 ± 0.0086 | 0.9852 ± 0.0003 | 0.8499 ± 0.0172 | 0.0097 ± 0.0000 | 0.9125 ± 0.0101 | 0.8606 ± 0.0141 |
| dynamický | 0.8278 ± 0.0073 | 0.8026 ± 0.0085 | 0.9797 ± 0.0005 | 0.6150 ± 0.0169 | 0.0097 ± 0.0000 | 0.7556 ± 0.0129 | 0.6741 ± 0.0132 |
| hybrid (každá vzorka) | 0.9704 ± 0.0012 | 0.9673 ± 0.0013 | 0.9867 ± 0.0000 | 0.9443 ± 0.0027 | 0.0097 ± 0.0000 | 0.9650 ± 0.0014 | 0.9400 ± 0.0023 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.2318 ± 0.0106 |
| statický | 0.1934 ± 0.0085 |
| dynamický | 0.3899 ± 0.0101 |
| hybrid (každá vzorka) | 0.3671 ± 0.0159 |

Podiel emulovaných: 37.95%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.0943 | 0.0425 | 0.8412 | 0.0026 | 0.9121 |
| 0.2000 | 0.2005 | 0.0775 | 0.8479 | 0.0025 | 0.9162 |
| 0.3000 | 0.2996 | 0.1090 | 0.8517 | 0.0025 | 0.9184 |
| 0.4000 | 0.3996 | 0.1251 | 0.8535 | 0.0025 | 0.9194 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **37.78%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
