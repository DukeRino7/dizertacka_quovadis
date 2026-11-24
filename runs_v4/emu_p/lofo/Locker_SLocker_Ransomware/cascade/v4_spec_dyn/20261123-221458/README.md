# V3 – špecialista `v4_spec_dyn` – beh `20261123-221458`

> Generované `src/cascade/specialist.py` (2026-11-23T22:15:14+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Locker/SLocker Ransomware**.

Vstup špecialistu: **dynamic** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/teachers/static_lightgbm/20261123-220732/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/static/lightgbm/20261123-185406`, dynamic `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/dynamic/lightgbm/20261123-220043`, hybrid `runs_v4/emu_p/lofo/Locker_SLocker_Ransomware/hybrid/lightgbm/20261123-220356`.

## Test – hlavný rozpočet 10% (emulované 11.46% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9327 ± 0.0049 | 0.0084 ± 0.0010 | 0.9600 ± 0.0021 | 0.5190 ± 0.0077 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9238 ± 0.0011 | 0.0034 ± 0.0004 | 0.9583 ± 0.0004 | 0.4892 ± 0.0053 |
| statický LightGBM | 0.9154 ± 0.0028 | 0.0071 ± 0.0002 | 0.9515 ± 0.0017 | 0.5005 ± 0.0036 |
| dynamický LightGBM | 0.8079 ± 0.0061 | 0.0082 ± 0.0006 | 0.8888 ± 0.0035 | 0.2462 ± 0.0171 |
| hybrid LightGBM | 0.9395 ± 0.0023 | 0.0065 ± 0.0005 | 0.9648 ± 0.0009 | 0.5477 ± 0.0092 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.3462 ± 0.0064 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.3205 ± 0.0018 |
| statický LightGBM | 0.3239 ± 0.0049 |
| dynamický LightGBM | 0.1861 ± 0.0078 |
| hybrid LightGBM | 0.3545 ± 0.0041 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1146 | 0.9327 | 0.0084 | 0.9238 | 0.0034 | 0.5190 |
| 0.2 | 0.2123 | 0.9314 | 0.0077 | 0.9261 | 0.0035 | 0.5087 |
| 0.3 | 0.3101 | 0.9307 | 0.0077 | 0.9269 | 0.0035 | 0.5056 |
| 0.4 | 0.4460 | 0.9297 | 0.0077 | 0.9274 | 0.0035 | 0.5056 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
