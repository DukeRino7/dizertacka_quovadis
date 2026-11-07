# V3 – špecialista `v3_spec` – beh `20261107-173351`

> Generované `src/cascade/specialist.py` (2026-11-07T17:34:10+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **coinminer**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/coinminer/teachers/static_lightgbm/20261104-005459/train_oof.parquet`). Komponenty: static `runs_v2/lofo/coinminer/static/lightgbm/20261103-232852`, dynamic `runs_v2/lofo/coinminer/dynamic/lightgbm/20261103-234518`, hybrid `runs_v2/lofo/coinminer/hybrid/lightgbm/20261104-001521`.

## Test – hlavný rozpočet 10% (emulované 26.52% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9218 ± 0.0030 | 0.0060 ± 0.0013 | 0.9568 ± 0.0011 | 0.6035 ± 0.0055 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9174 ± 0.0018 | 0.0040 ± 0.0006 | 0.9553 ± 0.0007 | 0.5986 ± 0.0016 |
| statický LightGBM | 0.9193 ± 0.0005 | 0.0053 ± 0.0005 | 0.9557 ± 0.0002 | 0.6006 ± 0.0012 |
| dynamický LightGBM | 0.5958 ± 0.0010 | 0.0141 ± 0.0005 | 0.7412 ± 0.0009 | 0.4986 ± 0.0012 |
| hybrid LightGBM | 0.9175 ± 0.0043 | 0.0055 ± 0.0013 | 0.9547 ± 0.0018 | 0.5966 ± 0.0085 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.8768 ± 0.0030 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8617 ± 0.0025 |
| statický LightGBM | 0.8650 ± 0.0061 |
| dynamický LightGBM | 0.2556 ± 0.0013 |
| hybrid LightGBM | 0.8711 ± 0.0072 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2652 | 0.9218 | 0.0060 | 0.9174 | 0.0040 | 0.6035 |
| 0.2 | 0.4176 | 0.9218 | 0.0060 | 0.9174 | 0.0040 | 0.6035 |
| 0.3 | 0.6078 | 0.9215 | 0.0060 | 0.9174 | 0.0040 | 0.6035 |
| 0.4 | 0.7278 | 0.9215 | 0.0060 | 0.9174 | 0.0040 | 0.6035 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
