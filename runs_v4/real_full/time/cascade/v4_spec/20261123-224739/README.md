# V3 – špecialista `v4_spec` – beh `20261123-224739`

> Generované `src/cascade/specialist.py` (2026-11-23T22:47:56+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Časový test (rozdelenie V1).

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/time/teachers/static_lightgbm/20261123-224036/train_oof.parquet`). Komponenty: static `runs_v4/real_full/time/static/lightgbm/20261123-223043`, dynamic `runs_v4/real_full/time/dynamic/lightgbm/20261123-223305`, hybrid `runs_v4/real_full/time/hybrid/lightgbm/20261123-223543`.

## Test – hlavný rozpočet 10% (emulované 37.88% súborov)
| prístup | recall_tpr | fpr | f1 |
|---|---|---|---|
| kaskáda so špecialistom | 0.8626 ± 0.0031 | 0.0079 ± 0.0003 | 0.9241 ± 0.0018 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8412 ± 0.0023 | 0.0036 ± 0.0004 | 0.9128 ± 0.0013 |
| statický LightGBM | 0.7456 ± 0.0576 | 0.0062 ± 0.0006 | 0.8518 ± 0.0370 |
| dynamický LightGBM | 0.6383 ± 0.0098 | 0.0091 ± 0.0008 | 0.7768 ± 0.0071 |
| hybrid LightGBM | 0.8853 ± 0.0018 | 0.0075 ± 0.0003 | 0.9371 ± 0.0011 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |
|---|---|---|---|---|---|
| 0.1 | 0.3788 | 0.8626 | 0.0079 | 0.8412 | 0.0036 |
| 0.2 | 0.5215 | 0.8675 | 0.0084 | 0.8468 | 0.0034 |
| 0.3 | 0.6023 | 0.8719 | 0.0086 | 0.8506 | 0.0035 |
| 0.4 | 0.6644 | 0.8731 | 0.0087 | 0.8538 | 0.0035 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
