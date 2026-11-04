# static/lightgbm – beh `20261103-211252`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/static/lightgbm/20261101-215345`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.017398074711291726, "num_leaves": 461, "min_child_samples": 101, "feature_fraction": 0.9576492590949324, "bagging_fraction": 0.9474136752138245, "lambda_l1": 0.002404915432737351, "lambda_l2": 1.9809253750493907}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9994 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.9996 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9985 ± 0.0000 | 0.9905 ± 0.0017 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9896 ± 0.0004 | 0.9630 ± 0.0013 |
| log loss | 0.0002 ± 0.0000 | 0.0117 ± 0.0002 | 0.0474 ± 0.0006 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0032 ± 0.0000 | 0.0123 ± 0.0002 |

Rozdiel ROC-AUC train − validácia: **0.0001** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9956 ± 0.0002 | 0.9893 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9947 ± 0.0002 | 0.9898 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9944 ± 0.0003 | 0.9957 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9985 ± 0.0000 | 0.9846 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0090 ± 0.0004 | 0.0050 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9964 ± 0.0001 | 0.9901 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9907 ± 0.0003 | 0.9786 ± 0.0001 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9957 ± 0.0003 | 0.9844 ± 0.0004 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9956 ± 0.0004 | 0.9854 ± 0.0003 |
| precision | 1.0000 ± 0.0000 | 0.9968 ± 0.0004 | 0.9981 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9962 ± 0.0001 | 0.9730 ± 0.0005 |
| FPR | 0.0000 ± 0.0000 | 0.0051 ± 0.0006 | 0.0022 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9965 ± 0.0003 | 0.9854 ± 0.0003 |
| MCC | 1.0000 ± 0.0000 | 0.9910 ± 0.0007 | 0.9690 ± 0.0007 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 267.2 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 591 589 |
| veľkosť modelu na disku | 34.72 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.362 ms (p95 0.454) |
| CPU priepustnosť (24 vlákien) | 36 722 vzoriek/s |

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
