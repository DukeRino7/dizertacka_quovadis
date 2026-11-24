# V3 – špecialista `v4_spec` – beh `20261123-214434`

> Generované `src/cascade/specialist.py` (2026-11-23T21:45:07+01:00). Plán: `docs/12_plan_v3.md`. Seedy [0, 1, 2], priemer ± sm. odchýlka.
> Prahy, eskalácia a prah špecialistu sú z validácie; test sa na nič nenastavuje.
> Zero-day: vynechaná rodina **Boxer**.

Vstup špecialistu: **hybrid** + log-odds statického skóre; tréning na 20% tréningu najbližšie
prahu (OOF skóre `runs_v4/emu_p/lofo/Boxer/teachers/static_lightgbm/20261123-213709/train_oof.parquet`). Komponenty: static `runs_v4/emu_p/lofo/Boxer/static/lightgbm/20261123-011538`, dynamic `runs_v4/emu_p/lofo/Boxer/dynamic/lightgbm/20261123-212946`, hybrid `runs_v4/emu_p/lofo/Boxer/hybrid/lightgbm/20261123-213325`.

## Test – hlavný rozpočet 10% (emulované 14.20% súborov)
| prístup | recall_tpr | fpr | f1 | tpr_family |
|---|---|---|---|---|
| kaskáda so špecialistom | 0.9538 ± 0.0009 | 0.0069 ± 0.0004 | 0.9721 ± 0.0006 | 0.9422 ± 0.0028 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9391 ± 0.0020 | 0.0031 ± 0.0004 | 0.9667 ± 0.0008 | 0.9163 ± 0.0094 |
| statický LightGBM | 0.9283 ± 0.0028 | 0.0056 ± 0.0005 | 0.9594 ± 0.0013 | 0.9088 ± 0.0041 |
| dynamický LightGBM | 0.7618 ± 0.0027 | 0.0091 ± 0.0005 | 0.8593 ± 0.0014 | 0.3535 ± 0.0122 |
| hybrid LightGBM | 0.9518 ± 0.0032 | 0.0056 ± 0.0005 | 0.9718 ± 0.0014 | 0.9323 ± 0.0075 |

## Januárové vzorky vynechanej rodiny (TPR)
| prístup | TPR |
|---|---|
| kaskáda so špecialistom | 0.9487 ± 0.0009 |
| kaskáda B-baselines (rovnaký rozpočet) | 0.9010 ± 0.0053 |
| statický LightGBM | 0.9037 ± 0.0030 |
| dynamický LightGBM | 0.3483 ± 0.0156 |
| hybrid LightGBM | 0.9267 ± 0.0027 |

## Krivka rozpočtu (test, priemer cez seedy)
| rozpočet (validácia) | emulované (test) | TPR špecialista | FPR špecialista | TPR B-baselines | FPR B-baselines |TPR vynech. rodiny špecialista |
|---|---|---|---|---|---|---|
| 0.1 | 0.1420 | 0.9538 | 0.0069 | 0.9391 | 0.0031 | 0.9422 |
| 0.2 | 0.2366 | 0.9551 | 0.0069 | 0.9412 | 0.0032 | 0.9422 |
| 0.3 | 0.3387 | 0.9556 | 0.0067 | 0.9421 | 0.0032 | 0.9422 |
| 0.4 | 0.4322 | 0.9559 | 0.0068 | 0.9429 | 0.0032 | 0.9422 |

## Výpočtové nároky
_Výpočtové nároky sa merajú iba v časovom teste (`--benchmark`)._
