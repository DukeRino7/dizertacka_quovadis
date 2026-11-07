# V3 – špecialista `v3_spec` – beh `20261107-173007`

> Generované `src/cascade/specialist.py` (2026-11-07T17:30:40+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Časový test (rozdelenie V1).

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_final/teachers/static_lightgbm/20261102-211118/train_oof.parquet`). Komponenty: static `runs_final/static/lightgbm/20261101-215345`, dynamic `runs_final/dynamic/lightgbm/20261102-003953`, hybrid `runs_final/hybrid/lightgbm/20261102-052826`.

## Test – hlavný rozpočet 10% (emulované 21.50% súborov)
| prístup | recall_tpr | fpr | f1 |
|---|---|---|---|
| kaskáda so špecialistom | 0.9891 ± 0.0040 | 0.0052 ± 0.0006 | 0.9923 ± 0.0021 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9831 ± 0.0018 | 0.0039 ± 0.0001 | 0.9898 ± 0.0009 |
| statický LightGBM | 0.9843 ± 0.0004 | 0.0048 ± 0.0002 | 0.9900 ± 0.0003 |
| dynamický LightGBM | 0.6572 ± 0.0069 | 0.0198 ± 0.0046 | 0.7852 ± 0.0032 |
| hybrid LightGBM | 0.9842 ± 0.0036 | 0.0047 ± 0.0002 | 0.9901 ± 0.0017 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |
|---|---|---|---|---|---|
| 0.1 | 0.2150 | 0.9891 | 0.0052 | 0.9831 | 0.0039 |
| 0.2 | 0.3977 | 0.9891 | 0.0052 | 0.9831 | 0.0039 |
| 0.3 | 0.5522 | 0.9891 | 0.0052 | 0.9831 | 0.0039 |
| 0.4 | 0.6938 | 0.9891 | 0.0052 | 0.9831 | 0.0039 |

## Výpočtové nároky
CPU ms/vz. (dávka): statický 0.6786 + 21.5% × špecialista 0.0870 = **0.6973** (odhad zo súčtu komponentov).
