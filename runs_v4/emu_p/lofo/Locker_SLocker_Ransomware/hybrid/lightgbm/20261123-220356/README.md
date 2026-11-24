# hybrid/lightgbm – beh `20261123-220356`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.021805367982090686, "num_leaves": 214, "min_child_samples": 11, "feature_fraction": 0.7934614803684483, "bagging_fraction": 0.9747297177039957, "lambda_l1": 3.6112431454858456e-05, "lambda_l2": 1.814656418208834e-05}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9959 ± 0.0001 | 0.9937 ± 0.0002 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9959 ± 0.0001 | 0.9939 ± 0.0002 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9612 ± 0.0014 | 0.9466 ± 0.0032 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8515 ± 0.0157 | 0.8847 ± 0.0090 |
| log loss | 0.0016 ± 0.0015 | 0.0742 ± 0.0041 | 0.1128 ± 0.0091 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0172 ± 0.0001 | 0.0245 ± 0.0002 |

Rozdiel ROC-AUC train − validácia: **0.0041** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9778 ± 0.0005 | 0.9693 ± 0.0008 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9758 ± 0.0006 | 0.9665 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9872 ± 0.0002 | 0.9915 ± 0.0007 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9612 ± 0.0014 | 0.9395 ± 0.0023 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0002 | 0.0065 ± 0.0005 |
| F1 | 1.0000 ± 0.0000 | 0.9740 ± 0.0006 | 0.9648 ± 0.0009 |
| MCC | 1.0000 ± 0.0000 | 0.9549 ± 0.0010 | 0.9386 ± 0.0014 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9784 ± 0.0003 | 0.9710 ± 0.0009 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9775 ± 0.0003 | 0.9693 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9789 ± 0.0008 | 0.9826 ± 0.0014 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9710 ± 0.0008 | 0.9522 ± 0.0008 |
| FPR | 0.0000 ± 0.0000 | 0.0160 ± 0.0007 | 0.0137 ± 0.0011 |
| F1 | 1.0000 ± 0.0000 | 0.9749 ± 0.0003 | 0.9672 ± 0.0010 |
| MCC | 1.0000 ± 0.0000 | 0.9560 ± 0.0006 | 0.9416 ± 0.0019 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 15.4 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 324 093 |
| veľkosť modelu na disku | 18.11 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.128 ms (p95 0.150) |
| CPU priepustnosť (24 vlákien) | 104 288 vzoriek/s |

## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
|  | ![učenie](plots/learning_curve.png) |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
