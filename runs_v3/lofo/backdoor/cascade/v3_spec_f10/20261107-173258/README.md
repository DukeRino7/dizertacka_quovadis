# V3 – špecialista `v3_spec_f10` – beh `20261107-173258`

> Generované `src/cascade/specialist.py` (2026-11-07T17:33:12+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **backdoor**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 10% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/backdoor/teachers/static_lightgbm/20261103-225240/train_oof.parquet`). Komponenty: static `runs_v2/lofo/backdoor/static/lightgbm/20261103-211252`, dynamic `runs_v2/lofo/backdoor/dynamic/lightgbm/20261103-212927`, hybrid `runs_v2/lofo/backdoor/hybrid/lightgbm/20261103-220506`.

## Test – hlavný rozpočet 10% (emulované 21.75% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9851 ± 0.0019 | 0.0054 ± 0.0009 | 0.9902 ± 0.0010 | 0.9832 ± 0.0029 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9811 ± 0.0011 | 0.0040 ± 0.0006 | 0.9888 ± 0.0003 | 0.9820 ± 0.0018 |
| statický LightGBM | 0.9846 ± 0.0003 | 0.0050 ± 0.0002 | 0.9901 ± 0.0001 | 0.9835 ± 0.0005 |
| dynamický LightGBM | 0.6083 ± 0.0028 | 0.0146 ± 0.0007 | 0.7507 ± 0.0020 | 0.4223 ± 0.0119 |
| hybrid LightGBM | 0.9842 ± 0.0032 | 0.0047 ± 0.0008 | 0.9900 ± 0.0013 | 0.9864 ± 0.0057 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9913 ± 0.0028 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9891 ± 0.0056 |
| statický LightGBM | 0.9931 ± 0.0022 |
| dynamický LightGBM | 0.4985 ± 0.0167 |
| hybrid LightGBM | 0.9916 ± 0.0049 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2175 | 0.9851 | 0.0054 | 0.9811 | 0.0040 | 0.9832 |
| 0.2 | 0.3619 | 0.9851 | 0.0054 | 0.9811 | 0.0040 | 0.9832 |
| 0.3 | 0.5610 | 0.9851 | 0.0054 | 0.9811 | 0.0040 | 0.9832 |
| 0.4 | 0.7324 | 0.9851 | 0.0054 | 0.9811 | 0.0040 | 0.9832 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
