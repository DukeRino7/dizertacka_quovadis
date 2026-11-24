# V3 – špecialista `v4_spec_dyn` – beh `20261123-190532`

> Generované `src/cascade/specialist.py` (2026-11-23T19:05:41+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Locker/SLocker Ransomware**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/real_p/lofo/Locker_SLocker_Ransomware/teachers/static_lightgbm/20261123-190018/train_oof.parquet`). Komponenty: static `runs_v4/real_p/lofo/Locker_SLocker_Ransomware/static/lightgbm/20261123-185406`, dynamic `runs_v4/real_p/lofo/Locker_SLocker_Ransomware/dynamic/lightgbm/20261123-185604`, hybrid `runs_v4/real_p/lofo/Locker_SLocker_Ransomware/hybrid/lightgbm/20261123-185825`.

## Test – hlavný rozpočet 10% (emulované 11.46% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9449 ± 0.0018 | 0.0074 ± 0.0007 | 0.9671 ± 0.0007 | 0.5467 ± 0.0124 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9346 ± 0.0017 | 0.0032 ± 0.0002 | 0.9642 ± 0.0010 | 0.5221 ± 0.0047 |
| statický LightGBM | 0.9154 ± 0.0028 | 0.0071 ± 0.0002 | 0.9515 ± 0.0017 | 0.5005 ± 0.0036 |
| dynamický LightGBM | 0.8318 ± 0.0065 | 0.0083 ± 0.0009 | 0.9032 ± 0.0033 | 0.3887 ± 0.0247 |
| hybrid LightGBM | 0.9513 ± 0.0009 | 0.0070 ± 0.0004 | 0.9708 ± 0.0007 | 0.6308 ± 0.0134 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.3751 ± 0.0067 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.3452 ± 0.0015 |
| statický LightGBM | 0.3239 ± 0.0049 |
| dynamický LightGBM | 0.5204 ± 0.0140 |
| hybrid LightGBM | 0.5070 ± 0.0749 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1146 | 0.9449 | 0.0074 | 0.9346 | 0.0032 | 0.5467 |
| 0.2 | 0.2123 | 0.9488 | 0.0080 | 0.9375 | 0.0035 | 0.5621 |
| 0.3 | 0.3101 | 0.9495 | 0.0075 | 0.9395 | 0.0035 | 0.5703 |
| 0.4 | 0.4460 | 0.9503 | 0.0076 | 0.9409 | 0.0035 | 0.5764 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
