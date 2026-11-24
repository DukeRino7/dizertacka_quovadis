# V3 – špecialista `v4_spec` – beh `20261123-191739`

> Generované `src/cascade/specialist.py` (2026-11-23T19:17:48+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **BankBot**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/lofo/BankBot/teachers/static_lightgbm/20261123-191216/train_oof.parquet`). Komponenty: static `runs_v4/real_p/lofo/BankBot/static/lightgbm/20261123-190600`, dynamic `runs_v4/real_p/lofo/BankBot/dynamic/lightgbm/20261123-190812`, hybrid `runs_v4/real_p/lofo/BankBot/hybrid/lightgbm/20261123-191024`.

## Test – hlavný rozpočet 10% (emulované 10.54% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9703 ± 0.0005 | 0.0087 ± 0.0005 | 0.9796 ± 0.0006 | 0.9918 ± 0.0000 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9615 ± 0.0001 | 0.0032 ± 0.0003 | 0.9784 ± 0.0002 | 0.9918 ± 0.0000 |
| statický LightGBM | 0.9447 ± 0.0033 | 0.0080 ± 0.0006 | 0.9667 ± 0.0016 | 0.9810 ± 0.0024 |
| dynamický LightGBM | 0.8325 ± 0.0032 | 0.0066 ± 0.0009 | 0.9046 ± 0.0017 | 0.7633 ± 0.0601 |
| hybrid LightGBM | 0.9726 ± 0.0017 | 0.0070 ± 0.0001 | 0.9818 ± 0.0008 | 0.9878 ± 0.0000 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9902 ± 0.0006 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9912 ± 0.0016 |
| statický LightGBM | 0.9851 ± 0.0006 |
| dynamický LightGBM | 0.7526 ± 0.0764 |
| hybrid LightGBM | 0.9942 ± 0.0006 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1054 | 0.9703 | 0.0087 | 0.9615 | 0.0032 | 0.9918 |
| 0.2 | 0.2023 | 0.9732 | 0.0088 | 0.9642 | 0.0034 | 0.9918 |
| 0.3 | 0.3018 | 0.9742 | 0.0088 | 0.9658 | 0.0035 | 0.9918 |
| 0.4 | 0.4043 | 0.9750 | 0.0089 | 0.9667 | 0.0035 | 0.9918 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
