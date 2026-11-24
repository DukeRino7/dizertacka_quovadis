# V3 – špecialista `v4_spec_dyn` – beh `20261123-185340`

> Generované `src/cascade/specialist.py` (2026-11-23T18:53:46+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **FakeInst**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/lofo/FakeInst/teachers/static_lightgbm/20261123-184824/train_oof.parquet`). Komponenty: static `runs_v4/real_p/lofo/FakeInst/static/lightgbm/20261123-184203`, dynamic `runs_v4/real_p/lofo/FakeInst/dynamic/lightgbm/20261123-184401`, hybrid `runs_v4/real_p/lofo/FakeInst/hybrid/lightgbm/20261123-184633`.

## Test – hlavný rozpočet 10% (emulované 11.17% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9681 ± 0.0012 | 0.0103 ± 0.0001 | 0.9775 ± 0.0006 | 0.9366 ± 0.0062 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9554 ± 0.0024 | 0.0034 ± 0.0009 | 0.9751 ± 0.0008 | 0.9069 ± 0.0095 |
| statický LightGBM | 0.9366 ± 0.0033 | 0.0075 ± 0.0014 | 0.9626 ± 0.0011 | 0.8459 ± 0.0153 |
| dynamický LightGBM | 0.8249 ± 0.0027 | 0.0068 ± 0.0004 | 0.8999 ± 0.0014 | 0.5845 ± 0.0122 |
| hybrid LightGBM | 0.9698 ± 0.0006 | 0.0068 ± 0.0011 | 0.9805 ± 0.0009 | 0.9577 ± 0.0023 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9170 ± 0.0062 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8901 ± 0.0053 |
| statický LightGBM | 0.8246 ± 0.0157 |
| dynamický LightGBM | 0.5583 ± 0.0101 |
| hybrid LightGBM | 0.9418 ± 0.0054 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1117 | 0.9681 | 0.0103 | 0.9554 | 0.0034 | 0.9366 |
| 0.2 | 0.2164 | 0.9704 | 0.0103 | 0.9577 | 0.0037 | 0.9366 |
| 0.3 | 0.3137 | 0.9713 | 0.0104 | 0.9596 | 0.0037 | 0.9343 |
| 0.4 | 0.4133 | 0.9715 | 0.0105 | 0.9604 | 0.0037 | 0.9311 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
