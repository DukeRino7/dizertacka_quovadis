# static/lightgbm – beh `20261101-215345`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** 30 dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, 97.1 min
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.017398074711291726, "num_leaves": 461, "min_child_samples": 101, "feature_fraction": 0.9576492590949324, "bagging_fraction": 0.9474136752138245, "lambda_l1": 0.002404915432737351, "lambda_l2": 1.9809253750493907}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9995 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9996 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9978 ± 0.0000 | 0.9943 ± 0.0001 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9900 ± 0.0005 | 0.9699 ± 0.0005 |
| log loss | 0.0001 ± 0.0000 | 0.0143 ± 0.0002 | 0.0397 ± 0.0008 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0034 ± 0.0000 | 0.0105 ± 0.0003 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9956 ± 0.0001 | 0.9893 ± 0.0003 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9945 ± 0.0001 | 0.9897 ± 0.0003 |
| precision | 1.0000 ± 0.0000 | 0.9957 ± 0.0001 | 0.9959 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9978 ± 0.0000 | 0.9843 ± 0.0004 |
| FPR | 0.0000 ± 0.0000 | 0.0089 ± 0.0002 | 0.0048 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9967 ± 0.0001 | 0.9900 ± 0.0003 |
| MCC | 1.0000 ± 0.0000 | 0.9900 ± 0.0002 | 0.9785 ± 0.0006 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9959 ± 0.0002 | 0.9862 ± 0.0009 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9958 ± 0.0002 | 0.9871 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9977 ± 0.0003 | 0.9980 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9962 ± 0.0003 | 0.9766 ± 0.0017 |
| FPR | 0.0000 ± 0.0000 | 0.0046 ± 0.0006 | 0.0023 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9970 ± 0.0001 | 0.9872 ± 0.0009 |
| MCC | 1.0000 ± 0.0000 | 0.9908 ± 0.0004 | 0.9726 ± 0.0018 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 376.0 s (priemer cez seedy) |
| ladenie spolu | 5826 s |
| počet parametrov / uzlov | 648 856 |
| veľkosť modelu na disku | 38.08 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.420 ms (p95 0.607) |
| CPU priepustnosť (24 vlákien) | 31 996 vzoriek/s |

## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
| ![ladenie](plots/hpo_history.png) | ![učenie](plots/learning_curve.png) |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
