# V3 – špecialista `v4_spec_dyn` – beh `20261122-230849`

> Generované `src/cascade/specialist.py` (2026-11-22T23:09:03+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **BankBot**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/lofo/BankBot/teachers/static_lightgbm/20261122-230028/train_oof.parquet`). Komponenty: static `runs_v4/real_full/lofo/BankBot/static/lightgbm/20261122-224851`, dynamic `runs_v4/real_full/lofo/BankBot/dynamic/lightgbm/20261122-225203`, hybrid `runs_v4/real_full/lofo/BankBot/hybrid/lightgbm/20261122-225455`.

## Test – hlavný rozpočet 10% (emulované 10.26% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9693 ± 0.0018 | 0.0083 ± 0.0014 | 0.9807 ± 0.0005 | 0.9923 ± 0.0000 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9613 ± 0.0009 | 0.0038 ± 0.0001 | 0.9786 ± 0.0005 | 0.9923 ± 0.0000 |
| statický LightGBM | 0.9436 ± 0.0012 | 0.0059 ± 0.0002 | 0.9684 ± 0.0006 | 0.9807 ± 0.0000 |
| dynamický LightGBM | 0.8636 ± 0.0022 | 0.0094 ± 0.0001 | 0.9227 ± 0.0012 | 0.7722 ± 0.0650 |
| hybrid LightGBM | 0.9739 ± 0.0003 | 0.0079 ± 0.0004 | 0.9833 ± 0.0001 | 0.9884 ± 0.0000 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9920 ± 0.0006 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9920 ± 0.0006 |
| statický LightGBM | 0.9855 ± 0.0010 |
| dynamický LightGBM | 0.7736 ± 0.0777 |
| hybrid LightGBM | 0.9958 ± 0.0006 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1026 | 0.9693 | 0.0083 | 0.9613 | 0.0038 | 0.9923 |
| 0.2 | 0.2042 | 0.9720 | 0.0076 | 0.9645 | 0.0038 | 0.9923 |
| 0.3 | 0.3056 | 0.9731 | 0.0078 | 0.9659 | 0.0041 | 0.9923 |
| 0.4 | 0.4059 | 0.9739 | 0.0079 | 0.9668 | 0.0041 | 0.9923 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
