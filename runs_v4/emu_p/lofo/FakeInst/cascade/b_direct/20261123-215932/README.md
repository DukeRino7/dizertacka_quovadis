# Kaskáda B `b_direct` – beh `20261123-215932`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T21:59:32+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/emu_p/lofo/FakeInst/students_static/mlp_kd/20261123-215606` |
| hybrid | `runs_v4/emu_p/lofo/FakeInst/hybrid/lightgbm/20261123-214927` |

Druhý stupeň: **hybrid**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0091, hi = 0.9992, seed 1: lo = 0.0073, hi = 0.9999, seed 2: lo = 0.0073, hi = 0.9981).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9761 ± 0.0006 | 0.9742 ± 0.0006 | 0.9909 ± 0.0003 | 0.9555 ± 0.0013 | 0.0072 ± 0.0002 | 0.9728 ± 0.0006 | 0.9520 ± 0.0011 |
| statický | 0.9317 ± 0.0021 | 0.9246 ± 0.0024 | 0.9902 ± 0.0014 | 0.8561 ± 0.0058 | 0.0069 ± 0.0010 | 0.9183 ± 0.0028 | 0.8669 ± 0.0036 |
| hybrid (každá vzorka) | 0.9768 ± 0.0005 | 0.9750 ± 0.0005 | 0.9912 ± 0.0005 | 0.9568 ± 0.0006 | 0.0069 ± 0.0004 | 0.9737 ± 0.0005 | 0.9535 ± 0.0010 |

- **emulované súbory: 36.59%** (ostatné rozhodne iba statický model); na hybrid ide 36.59% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 60
- validácia: emulované 36.44%, na hybrid 36.44%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9767 ± 0.0008 | 0.9746 ± 0.0009 | 0.9860 ± 0.0006 | 0.9593 ± 0.0014 | 0.0102 ± 0.0004 | 0.9725 ± 0.0010 | 0.9526 ± 0.0016 |
| statický | 0.9353 ± 0.0027 | 0.9262 ± 0.0031 | 0.9852 ± 0.0001 | 0.8621 ± 0.0063 | 0.0097 ± 0.0000 | 0.9195 ± 0.0036 | 0.8712 ± 0.0052 |
| hybrid (každá vzorka) | 0.9772 ± 0.0004 | 0.9750 ± 0.0004 | 0.9867 ± 0.0000 | 0.9598 ± 0.0009 | 0.0097 ± 0.0000 | 0.9731 ± 0.0005 | 0.9536 ± 0.0008 |

## Januárové vzorky vynechanej rodiny (iba malvér → TPR)
| prístup | TPR |
|---|---|
| kaskáda B | 0.8912 ± 0.0036 |
| statický | 0.7866 ± 0.0109 |
| hybrid (každá vzorka) | 0.8899 ± 0.0042 |

Podiel emulovaných: 53.12%

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.0921 | 0.0921 | 0.9108 | 0.0045 | 0.9506 |
| 0.2000 | 0.2006 | 0.2006 | 0.9360 | 0.0058 | 0.9634 |
| 0.3000 | 0.3087 | 0.3087 | 0.9500 | 0.0064 | 0.9704 |
| 0.4000 | 0.4166 | 0.4166 | 0.9533 | 0.0066 | 0.9721 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **36.59%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
