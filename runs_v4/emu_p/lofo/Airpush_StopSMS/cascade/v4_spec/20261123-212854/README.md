# V3 – špecialista `v4_spec` – beh `20261123-212854`

> Generované `src/cascade/specialist.py` (2026-11-23T21:29:14+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Airpush/StopSMS**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/lofo/Airpush_StopSMS/teachers/static_lightgbm/20261123-212224/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/lofo/Airpush_StopSMS/static/lightgbm/20261123-010336`, dynamic `runs_v4/emu_p/lofo/Airpush_StopSMS/dynamic/lightgbm/20261123-211603`, hybrid `runs_v4/emu_p/lofo/Airpush_StopSMS/hybrid/lightgbm/20261123-211909`.

## Test – hlavný rozpočet 10% (emulované 17.01% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.8793 ± 0.0085 | 0.0072 ± 0.0001 | 0.9314 ± 0.0048 | 0.6024 ± 0.0283 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.8690 ± 0.0021 | 0.0039 ± 0.0002 | 0.9276 ± 0.0011 | 0.5813 ± 0.0085 |
| statický LightGBM | 0.8502 ± 0.0033 | 0.0072 ± 0.0002 | 0.9147 ± 0.0018 | 0.5003 ± 0.0125 |
| dynamický LightGBM | 0.7652 ± 0.0024 | 0.0069 ± 0.0003 | 0.8628 ± 0.0015 | 0.5675 ± 0.0059 |
| hybrid LightGBM | 0.8829 ± 0.0030 | 0.0069 ± 0.0005 | 0.9336 ± 0.0015 | 0.6190 ± 0.0089 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.5958 ± 0.0318 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.5696 ± 0.0057 |
| statický LightGBM | 0.4739 ± 0.0097 |
| dynamický LightGBM | 0.5480 ± 0.0031 |
| hybrid LightGBM | 0.6160 ± 0.0067 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1701 | 0.8793 | 0.0072 | 0.8690 | 0.0039 | 0.6024 |
| 0.2 | 0.2673 | 0.8793 | 0.0072 | 0.8714 | 0.0039 | 0.6024 |
| 0.3 | 0.3597 | 0.8793 | 0.0072 | 0.8716 | 0.0039 | 0.6024 |
| 0.4 | 0.4544 | 0.8794 | 0.0072 | 0.8720 | 0.0039 | 0.6024 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
