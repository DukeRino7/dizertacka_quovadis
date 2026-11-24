# V3 – špecialista `v4_spec_dyn` – beh `20261123-010217`

> Generované `src/cascade/specialist.py` (2026-11-23T01:02:34+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Časový test (rozdelenie V1).

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/full/teachers/static_lightgbm/20261123-001942/train_oof.parquet`). Komponenty: static `runs_v4/real_p/full/static/lightgbm/20261122-231010`, dynamic `runs_v4/real_p/full/dynamic/lightgbm/20261122-233440`, hybrid `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912`.

## Test – hlavný rozpočet 10% (emulované 10.64% súborov)
| prístup | recall_tpr | fpr | f1 |
|---|---|---|---|
| kaskáda so špecialistom | 0.9696 ± 0.0007 | 0.0092 ± 0.0009 | 0.9789 ± 0.0007 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9603 ± 0.0020 | 0.0030 ± 0.0002 | 0.9779 ± 0.0010 |
| statický LightGBM | 0.9444 ± 0.0043 | 0.0080 ± 0.0009 | 0.9665 ± 0.0018 |
| dynamický LightGBM | 0.8455 ± 0.0023 | 0.0074 ± 0.0007 | 0.9118 ± 0.0010 |
| hybrid LightGBM | 0.9709 ± 0.0006 | 0.0062 ± 0.0003 | 0.9814 ± 0.0004 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |
|---|---|---|---|---|---|
| 0.1 | 0.1064 | 0.9696 | 0.0092 | 0.9603 | 0.0030 |
| 0.2 | 0.2008 | 0.9716 | 0.0086 | 0.9626 | 0.0032 |
| 0.3 | 0.3048 | 0.9719 | 0.0084 | 0.9643 | 0.0032 |
| 0.4 | 0.4006 | 0.9722 | 0.0085 | 0.9652 | 0.0032 |

## Výpočtové nároky
CPU ms/vz. (dávka): statický 0.2006 + 10.6% × špecialista 0.0109 = **0.2018** (odhad zo súčtu komponentov).
