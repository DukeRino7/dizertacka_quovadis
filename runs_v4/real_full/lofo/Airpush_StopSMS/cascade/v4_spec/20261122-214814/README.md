# V3 – špecialista `v4_spec` – beh `20261122-214814`

> Generované `src/cascade/specialist.py` (2026-11-22T21:48:45+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Airpush/StopSMS**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/lofo/Airpush_StopSMS/teachers/static_lightgbm/20261122-214036/train_oof.parquet`). Komponenty: static `runs_v4/real_full/lofo/Airpush_StopSMS/static/lightgbm/20261122-213043`, dynamic `runs_v4/real_full/lofo/Airpush_StopSMS/dynamic/lightgbm/20261122-213330`, hybrid `runs_v4/real_full/lofo/Airpush_StopSMS/hybrid/lightgbm/20261122-213609`.

## Test – hlavný rozpočet 10% (emulované 17.00% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9472 ± 0.0040 | 0.0098 ± 0.0006 | 0.9685 ± 0.0020 | 0.8084 ± 0.0165 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9314 ± 0.0035 | 0.0045 ± 0.0001 | 0.9625 ± 0.0019 | 0.7687 ± 0.0138 |
| statický LightGBM | 0.8746 ± 0.0062 | 0.0073 ± 0.0003 | 0.9299 ± 0.0034 | 0.5050 ± 0.0182 |
| dynamický LightGBM | 0.8666 ± 0.0024 | 0.0085 ± 0.0002 | 0.9248 ± 0.0013 | 0.8472 ± 0.0030 |
| hybrid LightGBM | 0.9558 ± 0.0003 | 0.0075 ± 0.0002 | 0.9741 ± 0.0001 | 0.8802 ± 0.0024 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.7968 ± 0.0181 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.7649 ± 0.0160 |
| statický LightGBM | 0.4982 ± 0.0189 |
| dynamický LightGBM | 0.8570 ± 0.0010 |
| hybrid LightGBM | 0.8798 ± 0.0027 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1700 | 0.9472 | 0.0098 | 0.9314 | 0.0045 | 0.8084 |
| 0.2 | 0.2643 | 0.9567 | 0.0100 | 0.9401 | 0.0046 | 0.8512 |
| 0.3 | 0.3640 | 0.9626 | 0.0102 | 0.9461 | 0.0048 | 0.8793 |
| 0.4 | 0.4582 | 0.9644 | 0.0102 | 0.9478 | 0.0048 | 0.8883 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
