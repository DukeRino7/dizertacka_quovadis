# V3 – špecialista `v4_spec_f10` – beh `20261122-212912`

> Generované `src/cascade/specialist.py` (2026-11-22T21:29:33+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Časový test (rozdelenie V1).

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 10% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/full/teachers/static_lightgbm/20261122-203152/train_oof.parquet`). Komponenty: static `runs_v4/real_full/full/static/lightgbm/20261122-184829`, dynamic `runs_v4/real_full/full/dynamic/lightgbm/20261122-191914`, hybrid `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`.

## Test – hlavný rozpočet 10% (emulované 10.31% súborov)
| prístup | recall_tpr | fpr | f1 |
|---|---|---|---|
| kaskáda so špecialistom | 0.9735 ± 0.0018 | 0.0094 ± 0.0012 | 0.9824 ± 0.0004 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9617 ± 0.0026 | 0.0038 ± 0.0003 | 0.9788 ± 0.0014 |
| statický LightGBM | 0.9459 ± 0.0040 | 0.0062 ± 0.0005 | 0.9695 ± 0.0019 |
| dynamický LightGBM | 0.8688 ± 0.0051 | 0.0090 ± 0.0010 | 0.9259 ± 0.0026 |
| hybrid LightGBM | 0.9724 ± 0.0006 | 0.0076 ± 0.0005 | 0.9826 ± 0.0005 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |
|---|---|---|---|---|---|
| 0.1 | 0.1031 | 0.9735 | 0.0094 | 0.9617 | 0.0038 |
| 0.2 | 0.1987 | 0.9761 | 0.0089 | 0.9639 | 0.0038 |
| 0.3 | 0.3026 | 0.9769 | 0.0095 | 0.9653 | 0.0040 |
| 0.4 | 0.4061 | 0.9772 | 0.0100 | 0.9661 | 0.0040 |

## Výpočtové nároky
CPU ms/vz. (dávka): statický 0.2054 + 10.3% × špecialista 0.2088 = **0.2269** (odhad zo súčtu komponentov).
