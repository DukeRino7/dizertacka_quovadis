# hybrid/lightgbm – beh `20261103-220506`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9994 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9995 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9977 ± 0.0000 | 0.9924 ± 0.0022 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9924 ± 0.0017 | 0.9461 ± 0.0021 |
| log loss | 0.0003 ± 0.0000 | 0.0120 ± 0.0003 | 0.0490 ± 0.0019 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0034 ± 0.0002 | 0.0132 ± 0.0010 |

Rozdiel ROC-AUC train − validácia: **0.0001** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9948 ± 0.0001 | 0.9893 ± 0.0014 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9940 ± 0.0001 | 0.9897 ± 0.0013 |
| precision | 1.0000 ± 0.0000 | 0.9939 ± 0.0001 | 0.9959 ± 0.0006 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9977 ± 0.0000 | 0.9842 ± 0.0032 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0002 | 0.0047 ± 0.0008 |
| F1 | 1.0000 ± 0.0000 | 0.9958 ± 0.0001 | 0.9900 ± 0.0013 |
| MCC | 1.0000 ± 0.0000 | 0.9891 ± 0.0002 | 0.9785 ± 0.0028 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9954 ± 0.0003 | 0.9826 ± 0.0051 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9953 ± 0.0003 | 0.9838 ± 0.0047 |
| precision | 1.0000 ± 0.0000 | 0.9966 ± 0.0003 | 0.9980 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9959 ± 0.0003 | 0.9698 ± 0.0095 |
| FPR | 0.0000 ± 0.0000 | 0.0053 ± 0.0004 | 0.0023 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9963 ± 0.0003 | 0.9837 ± 0.0049 |
| MCC | 1.0000 ± 0.0000 | 0.9903 ± 0.0007 | 0.9655 ± 0.0099 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 17.6 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 32 613 |
| veľkosť modelu na disku | 1.81 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.045 ms (p95 0.054) |
| CPU priepustnosť (24 vlákien) | 296 237 vzoriek/s |

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
