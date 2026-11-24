# V3 – špecialista `v4_spec_dyn` – beh `20261122-222844`

> Generované `src/cascade/specialist.py` (2026-11-22T22:28:57+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **FakeInst**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_full/lofo/FakeInst/teachers/static_lightgbm/20261122-222024/train_oof.parquet`). Komponenty: static `runs_v4/real_full/lofo/FakeInst/static/lightgbm/20261122-220910`, dynamic `runs_v4/real_full/lofo/FakeInst/dynamic/lightgbm/20261122-221211`, hybrid `runs_v4/real_full/lofo/FakeInst/hybrid/lightgbm/20261122-221513`.

## Test – hlavný rozpočet 10% (emulované 11.85% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9674 ± 0.0011 | 0.0080 ± 0.0004 | 0.9799 ± 0.0004 | 0.9203 ± 0.0109 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9575 ± 0.0019 | 0.0038 ± 0.0001 | 0.9766 ± 0.0009 | 0.8882 ± 0.0128 |
| statický LightGBM | 0.9427 ± 0.0003 | 0.0061 ± 0.0002 | 0.9678 ± 0.0002 | 0.8484 ± 0.0044 |
| dynamický LightGBM | 0.8548 ± 0.0027 | 0.0088 ± 0.0007 | 0.9178 ± 0.0016 | 0.6045 ± 0.0095 |
| hybrid LightGBM | 0.9699 ± 0.0011 | 0.0075 ± 0.0002 | 0.9814 ± 0.0007 | 0.9364 ± 0.0012 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9021 ± 0.0151 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8680 ± 0.0124 |
| statický LightGBM | 0.8172 ± 0.0012 |
| dynamický LightGBM | 0.5770 ± 0.0053 |
| hybrid LightGBM | 0.9198 ± 0.0033 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1185 | 0.9674 | 0.0080 | 0.9575 | 0.0038 | 0.9203 |
| 0.2 | 0.2134 | 0.9703 | 0.0082 | 0.9601 | 0.0037 | 0.9315 |
| 0.3 | 0.3147 | 0.9717 | 0.0085 | 0.9615 | 0.0039 | 0.9322 |
| 0.4 | 0.4184 | 0.9724 | 0.0088 | 0.9623 | 0.0039 | 0.9322 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
