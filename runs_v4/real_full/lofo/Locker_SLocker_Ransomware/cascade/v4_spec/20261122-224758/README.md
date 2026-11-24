# V3 – špecialista `v4_spec` – beh `20261122-224758`

> Generované `src/cascade/specialist.py` (2026-11-22T22:48:14+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Locker/SLocker Ransomware**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/teachers/static_lightgbm/20261122-223948/train_oof.parquet`). Komponenty: static `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/static/lightgbm/20261122-222917`, dynamic `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/dynamic/lightgbm/20261122-223201`, hybrid `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/hybrid/lightgbm/20261122-223452`.

## Test – hlavný rozpočet 10% (emulované 11.38% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9535 ± 0.0010 | 0.0082 ± 0.0009 | 0.9726 ± 0.0003 | 0.5272 ± 0.0072 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9404 ± 0.0008 | 0.0041 ± 0.0000 | 0.9675 ± 0.0004 | 0.4774 ± 0.0063 |
| statický LightGBM | 0.9234 ± 0.0019 | 0.0058 ± 0.0002 | 0.9576 ± 0.0011 | 0.4475 ± 0.0042 |
| dynamický LightGBM | 0.8514 ± 0.0021 | 0.0089 ± 0.0008 | 0.9158 ± 0.0009 | 0.3841 ± 0.0042 |
| hybrid LightGBM | 0.9541 ± 0.0001 | 0.0075 ± 0.0002 | 0.9732 ± 0.0001 | 0.5625 ± 0.0027 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.3850 ± 0.0044 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.3399 ± 0.0024 |
| statický LightGBM | 0.3166 ± 0.0012 |
| dynamický LightGBM | 0.5138 ± 0.0027 |
| hybrid LightGBM | 0.4087 ± 0.0029 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1138 | 0.9535 | 0.0082 | 0.9404 | 0.0041 | 0.5272 |
| 0.2 | 0.2075 | 0.9572 | 0.0084 | 0.9425 | 0.0040 | 0.5371 |
| 0.3 | 0.3162 | 0.9596 | 0.0091 | 0.9443 | 0.0042 | 0.5571 |
| 0.4 | 0.4193 | 0.9609 | 0.0093 | 0.9455 | 0.0043 | 0.5761 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
