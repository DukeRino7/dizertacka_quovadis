# V3 – špecialista `v4_spec_dyn` – beh `20261122-220838`

> Generované `src/cascade/specialist.py` (2026-11-22T22:08:49+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Boxer**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/lofo/Boxer/teachers/static_lightgbm/20261122-220007/train_oof.parquet`). Komponenty: static `runs_v4/real_full/lofo/Boxer/static/lightgbm/20261122-214926`, dynamic `runs_v4/real_full/lofo/Boxer/dynamic/lightgbm/20261122-215222`, hybrid `runs_v4/real_full/lofo/Boxer/hybrid/lightgbm/20261122-215508`.

## Test – hlavný rozpočet 10% (emulované 13.40% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9646 ± 0.0011 | 0.0090 ± 0.0007 | 0.9780 ± 0.0004 | 0.9324 ± 0.0035 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9453 ± 0.0094 | 0.0040 ± 0.0001 | 0.9701 ± 0.0049 | 0.7921 ± 0.0934 |
| statický LightGBM | 0.9250 ± 0.0101 | 0.0063 ± 0.0003 | 0.9582 ± 0.0053 | 0.7477 ± 0.0871 |
| dynamický LightGBM | 0.8265 ± 0.0064 | 0.0091 ± 0.0013 | 0.9010 ± 0.0033 | 0.4653 ± 0.0300 |
| hybrid LightGBM | 0.9687 ± 0.0005 | 0.0084 ± 0.0004 | 0.9804 ± 0.0001 | 0.9347 ± 0.0014 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9373 ± 0.0043 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.7895 ± 0.0857 |
| statický LightGBM | 0.7385 ± 0.0888 |
| dynamický LightGBM | 0.4809 ± 0.0344 |
| hybrid LightGBM | 0.9436 ± 0.0011 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1340 | 0.9646 | 0.0090 | 0.9453 | 0.0040 | 0.9324 |
| 0.2 | 0.2313 | 0.9678 | 0.0091 | 0.9486 | 0.0039 | 0.9347 |
| 0.3 | 0.3318 | 0.9696 | 0.0097 | 0.9501 | 0.0042 | 0.9417 |
| 0.4 | 0.4319 | 0.9697 | 0.0093 | 0.9511 | 0.0042 | 0.9394 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
