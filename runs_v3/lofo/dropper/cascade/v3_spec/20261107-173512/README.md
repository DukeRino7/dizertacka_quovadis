# V3 – špecialista `v3_spec` – beh `20261107-173512`

> Generované `src/cascade/specialist.py` (2026-11-07T17:35:34+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **dropper**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/dropper/teachers/static_lightgbm/20261104-030748/train_oof.parquet`). Komponenty: static `runs_v2/lofo/dropper/static/lightgbm/20261104-012654`, dynamic `runs_v2/lofo/dropper/dynamic/lightgbm/20261104-014114`, hybrid `runs_v2/lofo/dropper/hybrid/lightgbm/20261104-022110`.

## Test – hlavný rozpočet 10% (emulované 20.15% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9872 ± 0.0012 | 0.0052 ± 0.0005 | 0.9913 ± 0.0005 | 0.9497 ± 0.0046 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9831 ± 0.0014 | 0.0039 ± 0.0002 | 0.9898 ± 0.0007 | 0.9405 ± 0.0000 |
| statický LightGBM | 0.9829 ± 0.0034 | 0.0047 ± 0.0003 | 0.9894 ± 0.0016 | 0.9431 ± 0.0046 |
| dynamický LightGBM | 0.6950 ± 0.0044 | 0.0239 ± 0.0022 | 0.8104 ± 0.0022 | 0.6799 ± 0.0023 |
| hybrid LightGBM | 0.9848 ± 0.0022 | 0.0047 ± 0.0010 | 0.9904 ± 0.0007 | 0.9471 ± 0.0061 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9784 ± 0.0058 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9821 ± 0.0042 |
| statický LightGBM | 0.9791 ± 0.0046 |
| dynamický LightGBM | 0.6458 ± 0.0037 |
| hybrid LightGBM | 0.9796 ± 0.0017 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2015 | 0.9872 | 0.0052 | 0.9831 | 0.0039 | 0.9497 |
| 0.2 | 0.3498 | 0.9872 | 0.0052 | 0.9831 | 0.0039 | 0.9497 |
| 0.3 | 0.5306 | 0.9872 | 0.0052 | 0.9831 | 0.0039 | 0.9497 |
| 0.4 | 0.6755 | 0.9872 | 0.0052 | 0.9831 | 0.0039 | 0.9497 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
