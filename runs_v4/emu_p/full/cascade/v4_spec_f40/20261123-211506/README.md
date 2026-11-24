# V3 – špecialista `v4_spec_f40` – beh `20261123-211506`

> Generované `src/cascade/specialist.py` (2026-11-23T21:15:40+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Časový test (rozdelenie V1).

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 40% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/full/teachers/static_lightgbm/20261123-202903/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/full/static/lightgbm/20261122-231010`, dynamic `runs_v4/emu_p/full/dynamic/lightgbm/20261123-191933`, hybrid `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`.

## Test – hlavný rozpočet 10% (emulované 10.64% súborov)
| prístup | recall_tpr | fpr | f1 |
|---|---|---|---|
| kaskáda so špecialistom | 0.9616 ± 0.0003 | 0.0083 ± 0.0007 | 0.9753 ± 0.0006 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9522 ± 0.0013 | 0.0034 ± 0.0002 | 0.9734 ± 0.0006 |
| statický LightGBM | 0.9444 ± 0.0043 | 0.0080 ± 0.0009 | 0.9665 ± 0.0018 |
| dynamický LightGBM | 0.8381 ± 0.0018 | 0.0080 ± 0.0003 | 0.9071 ± 0.0010 |
| hybrid LightGBM | 0.9632 ± 0.0002 | 0.0060 ± 0.0001 | 0.9775 ± 0.0002 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |
|---|---|---|---|---|---|
| 0.1 | 0.1064 | 0.9616 | 0.0083 | 0.9522 | 0.0034 |
| 0.2 | 0.2008 | 0.9622 | 0.0080 | 0.9547 | 0.0036 |
| 0.3 | 0.3048 | 0.9612 | 0.0075 | 0.9558 | 0.0036 |
| 0.4 | 0.4006 | 0.9612 | 0.0075 | 0.9561 | 0.0036 |

## Výpočtové nároky
CPU ms/vz. (dávka): statický 0.2006 + 10.6% × špecialista 0.0258 = **0.2033** (odhad zo súčtu komponentov).
