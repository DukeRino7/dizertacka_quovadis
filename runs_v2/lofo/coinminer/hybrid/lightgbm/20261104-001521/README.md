# hybrid/lightgbm – beh `20261104-001521`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9973 ± 0.0002 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9978 ± 0.0002 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9974 ± 0.0004 | 0.9236 ± 0.0024 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9925 ± 0.0009 | 0.8736 ± 0.0082 |
| log loss | 0.0002 ± 0.0000 | 0.0142 ± 0.0009 | 0.2226 ± 0.0071 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0035 ± 0.0002 | 0.0519 ± 0.0017 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9949 ± 0.0004 | 0.9528 ± 0.0018 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9940 ± 0.0004 | 0.9560 ± 0.0016 |
| precision | 1.0000 ± 0.0000 | 0.9947 ± 0.0004 | 0.9950 ± 0.0011 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9974 ± 0.0004 | 0.9175 ± 0.0043 |
| FPR | 0.0000 ± 0.0000 | 0.0094 ± 0.0007 | 0.0055 ± 0.0013 |
| F1 | 1.0000 ± 0.0000 | 0.9960 ± 0.0003 | 0.9547 ± 0.0018 |
| MCC | 1.0000 ± 0.0000 | 0.9890 ± 0.0008 | 0.9088 ± 0.0031 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9957 ± 0.0005 | 0.9398 ± 0.0052 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9957 ± 0.0007 | 0.9444 ± 0.0048 |
| precision | 1.0000 ± 0.0000 | 0.9976 ± 0.0008 | 0.9984 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9956 ± 0.0000 | 0.8904 ± 0.0097 |
| FPR | 0.0000 ± 0.0000 | 0.0042 ± 0.0014 | 0.0016 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9966 ± 0.0004 | 0.9413 ± 0.0054 |
| MCC | 1.0000 ± 0.0000 | 0.9906 ± 0.0011 | 0.8861 ± 0.0093 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 17.1 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 28 924 |
| veľkosť modelu na disku | 1.62 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.041 ms (p95 0.055) |
| CPU priepustnosť (24 vlákien) | 285 976 vzoriek/s |

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
