# hybrid/lightgbm – beh `20261123-223543`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.018196998780495684, "num_leaves": 233, "min_child_samples": 23, "feature_fraction": 0.6390322800765896, "bagging_fraction": 0.9532240144545877, "lambda_l1": 0.008505404243799093, "lambda_l2": 0.007794186652208281}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9977 ± 0.0001 | 0.9861 ± 0.0004 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9979 ± 0.0000 | 0.9932 ± 0.0002 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9731 ± 0.0005 | 0.8996 ± 0.0056 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8942 ± 0.0098 | 0.7451 ± 0.0322 |
| log loss | 0.0009 ± 0.0002 | 0.0591 ± 0.0001 | 0.2985 ± 0.0068 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0143 ± 0.0001 | 0.0559 ± 0.0009 |

Rozdiel ROC-AUC train − validácia: **0.0023** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9820 ± 0.0002 | 0.9231 ± 0.0013 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9817 ± 0.0003 | 0.9389 ± 0.0010 |
| precision | 1.0000 ± 0.0000 | 0.9893 ± 0.0000 | 0.9954 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9731 ± 0.0005 | 0.8853 ± 0.0018 |
| FPR | 0.0000 ± 0.0000 | 0.0098 ± 0.0000 | 0.0075 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9812 ± 0.0003 | 0.9371 ± 0.0011 |
| MCC | 1.0000 ± 0.0000 | 0.9640 ± 0.0005 | 0.8487 ± 0.0023 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9818 ± 0.0004 | 0.9357 ± 0.0028 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9817 ± 0.0004 | 0.9476 ± 0.0022 |
| precision | 1.0000 ± 0.0000 | 0.9829 ± 0.0003 | 0.9928 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9794 ± 0.0006 | 0.9072 ± 0.0043 |
| FPR | 0.0000 ± 0.0000 | 0.0159 ± 0.0003 | 0.0120 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9811 ± 0.0004 | 0.9481 ± 0.0024 |
| MCC | 1.0000 ± 0.0000 | 0.9636 ± 0.0007 | 0.8702 ± 0.0052 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 19.3 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 368 745 |
| veľkosť modelu na disku | 20.54 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.124 ms (p95 0.159) |
| CPU priepustnosť (24 vlákien) | 112 518 vzoriek/s |

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
