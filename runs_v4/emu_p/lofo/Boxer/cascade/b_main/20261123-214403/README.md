# Kaskáda B `b_main` – beh `20261123-214403`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T21:44:03+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/Boxer/students_static/mlp_kd/20261123-214009` |
| dynamic | `runs_v4/emu_p/lofo/Boxer/students_dynamic/mlp_kd/20261123-214125` |
| hybrid | `runs_v4/emu_p/lofo/Boxer/hybrid/lightgbm/20261123-213325` |

Druhý stupeň: **dynamic**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0073, hi = 0.9999, seed 1: lo = 0.0088, hi = 0.9997, seed 2: lo = 0.0076, hi = 0.9997).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9420 ± 0.0019 | 0.9356 ± 0.0021 | 0.9964 ± 0.0004 | 0.8738 ± 0.0040 | 0.0026 ± 0.0002 | 0.9311 ± 0.0024 | 0.8871 ± 0.0037 |
| statický | 0.9032 ± 0.0144 | 0.8927 ± 0.0161 | 0.9905 ± 0.0007 | 0.7916 ± 0.0324 | 0.0062 ± 0.0005 | 0.8797 ± 0.0198 | 0.8148 ± 0.0261 |
| dynamický | 0.8157 ± 0.0036 | 0.7954 ± 0.0042 | 0.9837 ± 0.0028 | 0.5989 ± 0.0099 | 0.0081 ± 0.0015 | 0.7445 ± 0.0068 | 0.6596 ± 0.0053 |
| hybrid (každá vzorka) | 0.9753 ± 0.0011 | 0.9731 ± 0.0013 | 0.9928 ± 0.0007 | 0.9518 ± 0.0032 | 0.0056 ± 0.0005 | 0.9718 ± 0.0014 | 0.9505 ± 0.0022 |

- **emulované súbory: 42.60%** (ostatné rozhodne iba statický model); na hybrid ide 12.04% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 50
- validácia: emulované 39.20%, na hybrid 9.50%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9478 ± 0.0020 | 0.9382 ± 0.0024 | 0.9924 ± 0.0003 | 0.8811 ± 0.0049 | 0.0048 ± 0.0002 | 0.9335 ± 0.0027 | 0.8951 ± 0.0039 |
| statický | 0.9270 ± 0.0043 | 0.9142 ± 0.0051 | 0.9839 ± 0.0002 | 0.8382 ± 0.0102 | 0.0097 ± 0.0000 | 0.9052 ± 0.0061 | 0.8537 ± 0.0082 |
| dynamický | 0.8357 ± 0.0059 | 0.8043 ± 0.0071 | 0.9783 ± 0.0005 | 0.6183 ± 0.0143 | 0.0097 ± 0.0000 | 0.7577 ± 0.0109 | 0.6815 ± 0.0110 |
| hybrid (každá vzorka) | 0.9744 ± 0.0004 | 0.9712 ± 0.0006 | 0.9862 ± 0.0007 | 0.9518 ± 0.0016 | 0.0095 ± 0.0005 | 0.9687 ± 0.0006 | 0.9475 ± 0.0008 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.8234 ± 0.0768 |
| statický | 0.4517 ± 0.2493 |
| dynamický | 0.5671 ± 0.0032 |
| hybrid (každá vzorka) | 0.9267 ± 0.0027 |

Podiel emulovaných: 98.47%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.1235 | 0.0650 | 0.8535 | 0.0031 | 0.9191 |
| 0.2000 | 0.2341 | 0.1042 | 0.8669 | 0.0023 | 0.9273 |
| 0.3000 | 0.3320 | 0.1282 | 0.8728 | 0.0024 | 0.9306 |
| 0.4000 | 0.4346 | 0.1447 | 0.8734 | 0.0025 | 0.9309 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **42.60%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
