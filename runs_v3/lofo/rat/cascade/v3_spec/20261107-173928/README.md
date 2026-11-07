# V3 – špecialista `v3_spec` – beh `20261107-173928`

> Generované `src/cascade/specialist.py` (2026-11-07T17:39:48+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **rat**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/rat/teachers/static_lightgbm/20261104-180257/train_oof.parquet`). Komponenty: static `runs_v2/lofo/rat/static/lightgbm/20261104-080300`, dynamic `runs_v2/lofo/rat/dynamic/lightgbm/20261104-081647`, hybrid `runs_v2/lofo/rat/hybrid/lightgbm/20261104-172135`.

## Test – hlavný rozpočet 10% (emulované 22.74% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9799 ± 0.0033 | 0.0056 ± 0.0010 | 0.9875 ± 0.0013 | 0.9359 ± 0.0231 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9664 ± 0.0095 | 0.0036 ± 0.0004 | 0.9814 ± 0.0050 | 0.9152 ± 0.0040 |
| statický LightGBM | 0.9751 ± 0.0012 | 0.0046 ± 0.0003 | 0.9855 ± 0.0005 | 0.9234 ± 0.0040 |
| dynamický LightGBM | 0.6389 ± 0.0127 | 0.0149 ± 0.0004 | 0.7737 ± 0.0096 | 0.7846 ± 0.0000 |
| hybrid LightGBM | 0.9718 ± 0.0115 | 0.0043 ± 0.0008 | 0.9839 ± 0.0061 | 0.9473 ± 0.0156 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9725 ± 0.0078 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9603 ± 0.0012 |
| statický LightGBM | 0.9644 ± 0.0009 |
| dynamický LightGBM | 0.7743 ± 0.0000 |
| hybrid LightGBM | 0.9684 ± 0.0043 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2274 | 0.9799 | 0.0056 | 0.9664 | 0.0036 | 0.9359 |
| 0.2 | 0.4345 | 0.9799 | 0.0056 | 0.9664 | 0.0036 | 0.9359 |
| 0.3 | 0.6049 | 0.9799 | 0.0056 | 0.9664 | 0.0036 | 0.9359 |
| 0.4 | 0.7118 | 0.9799 | 0.0056 | 0.9664 | 0.0036 | 0.9359 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
