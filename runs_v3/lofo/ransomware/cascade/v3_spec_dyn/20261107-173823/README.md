# V3 – špecialista `v3_spec_dyn` – beh `20261107-173823`

> Generované `src/cascade/specialist.py` (2026-11-07T17:38:29+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **ransomware**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v2/lofo/ransomware/teachers/static_lightgbm/20261104-072441/train_oof.parquet`). Komponenty: static `runs_v2/lofo/ransomware/static/lightgbm/20261104-055157`, dynamic `runs_v2/lofo/ransomware/dynamic/lightgbm/20261104-060251`, hybrid `runs_v2/lofo/ransomware/hybrid/lightgbm/20261104-063626`.

## Test – hlavný rozpočet 10% (emulované 23.12% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9743 ± 0.0048 | 0.0047 ± 0.0001 | 0.9850 ± 0.0025 | 0.9596 ± 0.0144 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9796 ± 0.0010 | 0.0034 ± 0.0005 | 0.9883 ± 0.0007 | 0.9807 ± 0.0007 |
| statický LightGBM | 0.9805 ± 0.0020 | 0.0048 ± 0.0003 | 0.9882 ± 0.0009 | 0.9821 ± 0.0013 |
| dynamický LightGBM | 0.5928 ± 0.0124 | 0.0128 ± 0.0000 | 0.7393 ± 0.0097 | 0.3132 ± 0.0494 |
| hybrid LightGBM | 0.9836 ± 0.0017 | 0.0041 ± 0.0009 | 0.9900 ± 0.0007 | 0.9849 ± 0.0034 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9882 ± 0.0051 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9947 ± 0.0011 |
| statický LightGBM | 0.9950 ± 0.0011 |
| dynamický LightGBM | 0.0833 ± 0.0012 |
| hybrid LightGBM | 0.9969 ± 0.0002 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.2312 | 0.9743 | 0.0047 | 0.9796 | 0.0034 | 0.9596 |
| 0.2 | 0.4220 | 0.9743 | 0.0047 | 0.9796 | 0.0034 | 0.9596 |
| 0.3 | 0.5943 | 0.9743 | 0.0047 | 0.9796 | 0.0034 | 0.9596 |
| 0.4 | 0.7189 | 0.9743 | 0.0047 | 0.9796 | 0.0034 | 0.9596 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
