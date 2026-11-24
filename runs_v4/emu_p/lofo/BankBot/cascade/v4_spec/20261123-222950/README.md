# V3 – špecialista `v4_spec` – beh `20261123-222950`

> Generované `src/cascade/specialist.py` (2026-11-23T22:30:12+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **BankBot**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/lofo/BankBot/teachers/static_lightgbm/20261123-222257/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/lofo/BankBot/static/lightgbm/20261123-190600`, dynamic `runs_v4/emu_p/lofo/BankBot/dynamic/lightgbm/20261123-221537`, hybrid `runs_v4/emu_p/lofo/BankBot/hybrid/lightgbm/20261123-221915`.

## Test – hlavný rozpočet 10% (emulované 10.54% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9614 ± 0.0019 | 0.0081 ± 0.0009 | 0.9754 ± 0.0007 | 0.9864 ± 0.0062 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9515 ± 0.0007 | 0.0036 ± 0.0002 | 0.9729 ± 0.0005 | 0.9878 ± 0.0000 |
| statický LightGBM | 0.9447 ± 0.0033 | 0.0080 ± 0.0006 | 0.9667 ± 0.0016 | 0.9810 ± 0.0024 |
| dynamický LightGBM | 0.8382 ± 0.0048 | 0.0096 ± 0.0011 | 0.9062 ± 0.0022 | 0.8463 ± 0.0062 |
| hybrid LightGBM | 0.9608 ± 0.0016 | 0.0066 ± 0.0004 | 0.9759 ± 0.0010 | 0.9878 ± 0.0000 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9898 ± 0.0010 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9915 ± 0.0006 |
| statický LightGBM | 0.9851 ± 0.0006 |
| dynamický LightGBM | 0.8562 ± 0.0016 |
| hybrid LightGBM | 0.9915 ± 0.0006 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1054 | 0.9614 | 0.0081 | 0.9515 | 0.0036 | 0.9864 |
| 0.2 | 0.2023 | 0.9619 | 0.0081 | 0.9536 | 0.0038 | 0.9864 |
| 0.3 | 0.3018 | 0.9621 | 0.0081 | 0.9546 | 0.0038 | 0.9864 |
| 0.4 | 0.4043 | 0.9621 | 0.0082 | 0.9550 | 0.0038 | 0.9864 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
