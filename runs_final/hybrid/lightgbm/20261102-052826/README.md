# hybrid/lightgbm – beh `20261102-052826`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** 30 dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, 69.6 min
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9994 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9995 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9968 ± 0.0005 | 0.9915 ± 0.0015 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9901 ± 0.0015 | 0.9329 ± 0.0281 |
| log loss | 0.0008 ± 0.0008 | 0.0147 ± 0.0002 | 0.0477 ± 0.0035 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0038 ± 0.0001 | 0.0125 ± 0.0009 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9948 ± 0.0004 | 0.9893 ± 0.0018 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9938 ± 0.0004 | 0.9898 ± 0.0017 |
| precision | 1.0000 ± 0.0000 | 0.9955 ± 0.0003 | 0.9960 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9968 ± 0.0005 | 0.9842 ± 0.0036 |
| FPR | 0.0000 ± 0.0000 | 0.0091 ± 0.0006 | 0.0047 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9962 ± 0.0003 | 0.9901 ± 0.0017 |
| MCC | 1.0000 ± 0.0000 | 0.9883 ± 0.0009 | 0.9785 ± 0.0037 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9949 ± 0.0005 | 0.9833 ± 0.0045 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9948 ± 0.0006 | 0.9844 ± 0.0042 |
| precision | 1.0000 ± 0.0000 | 0.9972 ± 0.0003 | 0.9981 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9953 ± 0.0004 | 0.9710 ± 0.0082 |
| FPR | 0.0000 ± 0.0000 | 0.0057 ± 0.0007 | 0.0022 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9962 ± 0.0004 | 0.9843 ± 0.0043 |
| MCC | 1.0000 ± 0.0000 | 0.9885 ± 0.0012 | 0.9668 ± 0.0088 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 14.9 s (priemer cez seedy) |
| ladenie spolu | 4179 s |
| počet parametrov / uzlov | 29 103 |
| veľkosť modelu na disku | 1.64 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.041 ms (p95 0.052) |
| CPU priepustnosť (24 vlákien) | 306 145 vzoriek/s |

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
