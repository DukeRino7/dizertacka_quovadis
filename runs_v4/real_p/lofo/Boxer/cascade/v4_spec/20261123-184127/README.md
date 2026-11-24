# V3 – špecialista `v4_spec` – beh `20261123-184127`

> Generované `src/cascade/specialist.py` (2026-11-23T18:41:37+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Boxer**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/lofo/Boxer/teachers/static_lightgbm/20261123-183647/train_oof.parquet`). Komponenty: static `runs_v4/real_p/lofo/Boxer/static/lightgbm/20261123-011538`, dynamic `runs_v4/real_p/lofo/Boxer/dynamic/lightgbm/20261123-183231`, hybrid `runs_v4/real_p/lofo/Boxer/hybrid/lightgbm/20261123-183451`.

## Test – hlavný rozpočet 10% (emulované 14.20% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9626 ± 0.0015 | 0.0084 ± 0.0002 | 0.9758 ± 0.0009 | 0.9455 ± 0.0033 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9451 ± 0.0005 | 0.0029 ± 0.0004 | 0.9700 ± 0.0005 | 0.9055 ± 0.0102 |
| statický LightGBM | 0.9283 ± 0.0028 | 0.0056 ± 0.0005 | 0.9594 ± 0.0013 | 0.9088 ± 0.0041 |
| dynamický LightGBM | 0.7896 ± 0.0091 | 0.0076 ± 0.0007 | 0.8779 ± 0.0057 | 0.4875 ± 0.0579 |
| hybrid LightGBM | 0.9605 ± 0.0014 | 0.0067 ± 0.0009 | 0.9757 ± 0.0010 | 0.9290 ± 0.0086 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9497 ± 0.0051 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9168 ± 0.0059 |
| statický LightGBM | 0.9037 ± 0.0030 |
| dynamický LightGBM | 0.5195 ± 0.0520 |
| hybrid LightGBM | 0.9423 ± 0.0048 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1420 | 0.9626 | 0.0084 | 0.9451 | 0.0029 | 0.9455 |
| 0.2 | 0.2366 | 0.9658 | 0.0081 | 0.9484 | 0.0032 | 0.9422 |
| 0.3 | 0.3387 | 0.9669 | 0.0082 | 0.9501 | 0.0032 | 0.9412 |
| 0.4 | 0.4322 | 0.9680 | 0.0082 | 0.9513 | 0.0032 | 0.9417 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
