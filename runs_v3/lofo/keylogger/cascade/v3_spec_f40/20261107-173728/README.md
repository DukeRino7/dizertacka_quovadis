# V3 – špecialista `v3_spec_f40` – beh `20261107-173728`

> Generované `src/cascade/specialist.py` (2026-11-07T17:37:54+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **keylogger**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 40% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/keylogger/teachers/static_lightgbm/20261104-051704/train_oof.parquet`). Komponenty: static `runs_v2/lofo/keylogger/static/lightgbm/20261104-034747`, dynamic `runs_v2/lofo/keylogger/dynamic/lightgbm/20261104-040254`, hybrid `runs_v2/lofo/keylogger/hybrid/lightgbm/20261104-043557`.

## Test – hlavný rozpočet 10% (emulované 23.25% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9022 ± 0.0024 | 0.0046 ± 0.0009 | 0.9467 ± 0.0010 | 0.1928 ± 0.0207 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8777 ± 0.0014 | 0.0032 ± 0.0001 | 0.9335 ± 0.0008 | 0.1678 ± 0.0089 |
| statický LightGBM | 0.9065 ± 0.0031 | 0.0048 ± 0.0008 | 0.9489 ± 0.0014 | 0.2408 ± 0.0055 |
| dynamický LightGBM | 0.7120 ± 0.0130 | 0.0249 ± 0.0026 | 0.8216 ± 0.0078 | 0.1239 ± 0.0033 |
| hybrid LightGBM | 0.8775 ± 0.0032 | 0.0038 ± 0.0007 | 0.9331 ± 0.0016 | 0.1684 ± 0.0185 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.4178 ± 0.0157 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.4159 ± 0.0045 |
| statický LightGBM | 0.4291 ± 0.0045 |
| dynamický LightGBM | 0.3671 ± 0.0004 |
| hybrid LightGBM | 0.3950 ± 0.0089 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2325 | 0.9022 | 0.0046 | 0.8777 | 0.0032 | 0.1928 |
| 0.2 | 0.4117 | 0.9022 | 0.0046 | 0.8777 | 0.0032 | 0.1928 |
| 0.3 | 0.6531 | 0.9022 | 0.0046 | 0.8777 | 0.0032 | 0.1928 |
| 0.4 | 0.7303 | 0.9022 | 0.0046 | 0.8777 | 0.0032 | 0.1928 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
