# Kaskáda B `b_heavy` – beh `20261123-224730`

> Generované `src/cascade/evaluate_b.py` (2026-11-23T22:47:30+01:00). Seedy: [0, 1, 2]; hodnoty = priemer ± sm. odchýlka.
> Všetky prahy a pásmo neistoty sú z validácie; test sa na nič nenastavuje. Postup: `docs/09_plan_v2.md`.

| rola | beh |
|---|---|
| static | `runs_v4/real_full/time/students_static/mlp_kd/20261123-224256` |
| dynamic | `runs_v4/real_full/time/students_dynamic/mlp_kd/20261123-224410` |
| hybrid | `runs_v4/real_full/time/hybrid/mlp_large/20261123-223715` |

Druhý stupeň: **dynamic**. Pásmo neistoty statického modelu: FPR ≤ 0.1% nad `hi`,
najviac 1% malvéru validácie pod `lo` (seed 0: lo = 0.0203, hi = 0.9993, seed 1: lo = 0.0196, hi = 0.9994, seed 2: lo = 0.0190, hi = 0.9996).

## Test
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.8896 ± 0.0030 | 0.9141 ± 0.0023 | 0.9984 ± 0.0002 | 0.8307 ± 0.0047 | 0.0025 ± 0.0003 | 0.9068 ± 0.0028 | 0.7940 ± 0.0048 |
| statický | 0.8696 ± 0.0150 | 0.8974 ± 0.0112 | 0.9947 ± 0.0011 | 0.8028 ± 0.0242 | 0.0079 ± 0.0019 | 0.8884 ± 0.0143 | 0.7608 ± 0.0226 |
| dynamický | 0.7598 ± 0.0079 | 0.8125 ± 0.0060 | 0.9929 ± 0.0009 | 0.6333 ± 0.0125 | 0.0083 ± 0.0011 | 0.7733 ± 0.0093 | 0.6067 ± 0.0098 |
| hybrid (každá vzorka) | 0.8977 ± 0.0023 | 0.9192 ± 0.0019 | 0.9950 ± 0.0002 | 0.8462 ± 0.0035 | 0.0078 ± 0.0002 | 0.9146 ± 0.0021 | 0.8054 ± 0.0039 |

- **emulované súbory: 37.67%** (ostatné rozhodne iba statický model); na hybrid ide 12.48% súborov
- chyby pri istom rozhodnutí statického modelu (seed 0): 497
- validácia: emulované 33.30%, na hybrid 8.37%

## Validácia
| prístup | accuracy | balanced_accuracy | precision | recall_tpr | fpr | f1 | mcc |
|---|---|---|---|---|---|---|---|
| kaskáda B | 0.9640 ± 0.0036 | 0.9629 ± 0.0038 | 0.9939 ± 0.0007 | 0.9312 ± 0.0080 | 0.0054 ± 0.0007 | 0.9615 ± 0.0040 | 0.9296 ± 0.0068 |
| statický | 0.9356 ± 0.0086 | 0.9336 ± 0.0089 | 0.9881 ± 0.0002 | 0.8769 ± 0.0178 | 0.0098 ± 0.0000 | 0.9292 ± 0.0101 | 0.8758 ± 0.0158 |
| dynamický | 0.8734 ± 0.0061 | 0.8691 ± 0.0063 | 0.9863 ± 0.0004 | 0.7479 ± 0.0126 | 0.0097 ± 0.0002 | 0.8506 ± 0.0083 | 0.7658 ± 0.0105 |
| hybrid (každá vzorka) | 0.9747 ± 0.0011 | 0.9742 ± 0.0011 | 0.9893 ± 0.0003 | 0.9579 ± 0.0022 | 0.0096 ± 0.0003 | 0.9734 ± 0.0011 | 0.9498 ± 0.0021 |

## Krivka rozpočtu emulácie (test, priemer cez seedy)
| budget_val | emulation_rate | hybrid_rate | recall_tpr | fpr | f1 |
|---|---|---|---|---|---|
| 0.1000 | 0.1014 | 0.0503 | 0.8100 | 0.0030 | 0.8941 |
| 0.2000 | 0.2307 | 0.0974 | 0.8154 | 0.0025 | 0.8976 |
| 0.3000 | 0.3360 | 0.1296 | 0.8189 | 0.0024 | 0.8997 |
| 0.4000 | 0.4131 | 0.1481 | 0.8240 | 0.0024 | 0.9029 |

## Výpočtové nároky
Čas dynamickej analýzy (beh v emulátore alebo na zariadení) dataset neuvádza, preto sa neodhaduje. Úspora kaskády B = podiel súborov s dynamickou analýzou: **37.67%** (ostatné prístupy 100 %).

_Chýba benchmark niektorého komponentu (v zero-day behoch sa nemeria)._

![krivka](plots/budget_curve_test.png)
![rodiny](plots/emulation_by_family.png)
