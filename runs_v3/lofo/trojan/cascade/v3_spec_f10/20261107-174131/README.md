# V3 – špecialista `v3_spec_f10` – beh `20261107-174131`

> Generované `src/cascade/specialist.py` (2026-11-07T17:41:43+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **trojan**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 10% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/trojan/teachers/static_lightgbm/20261104-201459/train_oof.parquet`). Komponenty: static `runs_v2/lofo/trojan/static/lightgbm/20261104-184220`, dynamic `runs_v2/lofo/trojan/dynamic/lightgbm/20261104-190128`, hybrid `runs_v2/lofo/trojan/hybrid/lightgbm/20261104-193036`.

## Test – hlavný rozpočet 10% (emulované 22.10% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9716 ± 0.0060 | 0.0053 ± 0.0003 | 0.9834 ± 0.0030 | 0.8854 ± 0.0149 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9697 ± 0.0017 | 0.0030 ± 0.0004 | 0.9834 ± 0.0007 | 0.8731 ± 0.0060 |
| statický LightGBM | 0.9698 ± 0.0019 | 0.0035 ± 0.0001 | 0.9832 ± 0.0010 | 0.8719 ± 0.0048 |
| dynamický LightGBM | 0.7016 ± 0.0148 | 0.0239 ± 0.0018 | 0.8149 ± 0.0095 | 0.7432 ± 0.0149 |
| hybrid LightGBM | 0.9702 ± 0.0032 | 0.0042 ± 0.0008 | 0.9831 ± 0.0014 | 0.8786 ± 0.0147 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9321 ± 0.0119 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9233 ± 0.0055 |
| statický LightGBM | 0.9297 ± 0.0009 |
| dynamický LightGBM | 0.6712 ± 0.0097 |
| hybrid LightGBM | 0.9318 ± 0.0090 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2210 | 0.9716 | 0.0053 | 0.9697 | 0.0030 | 0.8854 |
| 0.2 | 0.4088 | 0.9696 | 0.0053 | 0.9697 | 0.0030 | 0.8854 |
| 0.3 | 0.5939 | 0.9688 | 0.0053 | 0.9697 | 0.0030 | 0.8854 |
| 0.4 | 0.7411 | 0.9676 | 0.0053 | 0.9697 | 0.0030 | 0.8854 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
