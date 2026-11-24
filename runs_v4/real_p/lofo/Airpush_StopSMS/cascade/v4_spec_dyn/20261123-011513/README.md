# V3 – špecialista `v4_spec_dyn` – beh `20261123-011513`

> Generované `src/cascade/specialist.py` (2026-11-23T01:15:17+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Airpush/StopSMS**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/lofo/Airpush_StopSMS/teachers/static_lightgbm/20261123-010945/train_oof.parquet`). Komponenty: static `runs_v4/real_p/lofo/Airpush_StopSMS/static/lightgbm/20261123-010336`, dynamic `runs_v4/real_p/lofo/Airpush_StopSMS/dynamic/lightgbm/20261123-010546`, hybrid `runs_v4/real_p/lofo/Airpush_StopSMS/hybrid/lightgbm/20261123-010804`.

## Test – hlavný rozpočet 10% (emulované 17.01% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9273 ± 0.0038 | 0.0089 ± 0.0007 | 0.9569 ± 0.0017 | 0.7691 ± 0.0140 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9150 ± 0.0016 | 0.0044 ± 0.0008 | 0.9529 ± 0.0005 | 0.7495 ± 0.0062 |
| statický LightGBM | 0.8502 ± 0.0033 | 0.0072 ± 0.0002 | 0.9147 ± 0.0018 | 0.5003 ± 0.0125 |
| dynamický LightGBM | 0.8466 ± 0.0020 | 0.0083 ± 0.0005 | 0.9119 ± 0.0008 | 0.8326 ± 0.0013 |
| hybrid LightGBM | 0.9489 ± 0.0013 | 0.0079 ± 0.0008 | 0.9689 ± 0.0004 | 0.8772 ± 0.0031 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.7598 ± 0.0100 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.7445 ± 0.0044 |
| statický LightGBM | 0.4739 ± 0.0097 |
| dynamický LightGBM | 0.8419 ± 0.0015 |
| hybrid LightGBM | 0.8720 ± 0.0019 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1701 | 0.9273 | 0.0089 | 0.9150 | 0.0044 | 0.7691 |
| 0.2 | 0.2673 | 0.9385 | 0.0089 | 0.9277 | 0.0044 | 0.8112 |
| 0.3 | 0.3597 | 0.9442 | 0.0087 | 0.9340 | 0.0044 | 0.8364 |
| 0.4 | 0.4544 | 0.9488 | 0.0086 | 0.9387 | 0.0044 | 0.8542 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
