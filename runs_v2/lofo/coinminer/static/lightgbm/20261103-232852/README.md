# static/lightgbm – beh `20261103-232852`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/static/lightgbm/20261101-215345`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.017398074711291726, "num_leaves": 461, "min_child_samples": 101, "feature_fraction": 0.9576492590949324, "bagging_fraction": 0.9474136752138245, "lambda_l1": 0.002404915432737351, "lambda_l2": 1.9809253750493907}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9977 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9982 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9977 ± 0.0000 | 0.9538 ± 0.0262 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9907 ± 0.0003 | 0.8756 ± 0.0016 |
| log loss | 0.0001 ± 0.0000 | 0.0143 ± 0.0004 | 0.1978 ± 0.0069 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0035 ± 0.0000 | 0.0483 ± 0.0007 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9955 ± 0.0005 | 0.9538 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9946 ± 0.0006 | 0.9570 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9952 ± 0.0007 | 0.9952 ± 0.0004 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9977 ± 0.0000 | 0.9193 ± 0.0005 |
| FPR | 0.0000 ± 0.0000 | 0.0085 ± 0.0013 | 0.0053 ± 0.0005 |
| F1 | 1.0000 ± 0.0000 | 0.9965 ± 0.0004 | 0.9557 ± 0.0002 |
| MCC | 1.0000 ± 0.0000 | 0.9902 ± 0.0010 | 0.9108 ± 0.0002 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9959 ± 0.0001 | 0.9448 ± 0.0036 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9958 ± 0.0002 | 0.9489 ± 0.0034 |
| precision | 1.0000 ± 0.0000 | 0.9976 ± 0.0001 | 0.9982 ± 0.0000 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9959 ± 0.0001 | 0.8997 ± 0.0067 |
| FPR | 0.0000 ± 0.0000 | 0.0042 ± 0.0002 | 0.0019 ± 0.0000 |
| F1 | 1.0000 ± 0.0000 | 0.9968 ± 0.0001 | 0.9464 ± 0.0037 |
| MCC | 1.0000 ± 0.0000 | 0.9910 ± 0.0003 | 0.8949 ± 0.0065 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 262.5 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 552 588 |
| veľkosť modelu na disku | 32.46 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.334 ms (p95 0.448) |
| CPU priepustnosť (24 vlákien) | 33 518 vzoriek/s |

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
