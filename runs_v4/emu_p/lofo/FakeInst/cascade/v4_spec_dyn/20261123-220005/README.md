# V3 – špecialista `v4_spec_dyn` – beh `20261123-220005`

> Generované `src/cascade/specialist.py` (2026-11-23T22:00:19+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **FakeInst**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/lofo/FakeInst/teachers/static_lightgbm/20261123-215302/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/lofo/FakeInst/static/lightgbm/20261123-184203`, dynamic `runs_v4/emu_p/lofo/FakeInst/dynamic/lightgbm/20261123-214549`, hybrid `runs_v4/emu_p/lofo/FakeInst/hybrid/lightgbm/20261123-214927`.

## Test – hlavný rozpočet 10% (emulované 11.17% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9478 ± 0.0015 | 0.0070 ± 0.0004 | 0.9689 ± 0.0006 | 0.8568 ± 0.0070 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9409 ± 0.0024 | 0.0038 ± 0.0003 | 0.9672 ± 0.0012 | 0.8302 ± 0.0138 |
| statický LightGBM | 0.9366 ± 0.0033 | 0.0075 ± 0.0014 | 0.9626 ± 0.0011 | 0.8459 ± 0.0153 |
| dynamický LightGBM | 0.8027 ± 0.0017 | 0.0088 ± 0.0005 | 0.8853 ± 0.0008 | 0.3560 ± 0.0059 |
| hybrid LightGBM | 0.9568 ± 0.0006 | 0.0069 ± 0.0004 | 0.9737 ± 0.0005 | 0.9147 ± 0.0036 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.8382 ± 0.0077 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8085 ± 0.0099 |
| statický LightGBM | 0.8246 ± 0.0157 |
| dynamický LightGBM | 0.3532 ± 0.0080 |
| hybrid LightGBM | 0.8899 ± 0.0042 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1117 | 0.9478 | 0.0070 | 0.9409 | 0.0038 | 0.8568 |
| 0.2 | 0.2164 | 0.9472 | 0.0069 | 0.9431 | 0.0038 | 0.8545 |
| 0.3 | 0.3137 | 0.9473 | 0.0069 | 0.9439 | 0.0038 | 0.8545 |
| 0.4 | 0.4133 | 0.9472 | 0.0069 | 0.9444 | 0.0039 | 0.8545 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
