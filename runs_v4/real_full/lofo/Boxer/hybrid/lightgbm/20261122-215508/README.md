# hybrid/lightgbm – beh `20261122-215508`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.018196998780495684, "num_leaves": 233, "min_child_samples": 23, "feature_fraction": 0.6390322800765896, "bagging_fraction": 0.9532240144545877, "lambda_l1": 0.008505404243799093, "lambda_l2": 0.007794186652208281}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9973 ± 0.0001 | 0.9980 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9979 ± 0.0000 | 0.9985 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9719 ± 0.0004 | 0.9726 ± 0.0004 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9083 ± 0.0050 | 0.9148 ± 0.0089 |
| log loss | 0.0016 ± 0.0006 | 0.0604 ± 0.0011 | 0.0563 ± 0.0010 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0148 ± 0.0001 | 0.0144 ± 0.0000 |

Rozdiel ROC-AUC train − validácia: **0.0027** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9810 ± 0.0001 | 0.9795 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9812 ± 0.0001 | 0.9802 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9906 ± 0.0005 | 0.9923 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9719 ± 0.0004 | 0.9687 ± 0.0005 |
| FPR | 0.0000 ± 0.0000 | 0.0095 ± 0.0005 | 0.0084 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9811 ± 0.0001 | 0.9804 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9623 ± 0.0002 | 0.9592 ± 0.0003 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9811 ± 0.0001 | 0.9818 ± 0.0002 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9811 ± 0.0001 | 0.9821 ± 0.0002 |
| precision | 1.0000 ± 0.0000 | 0.9837 ± 0.0008 | 0.9886 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9789 ± 0.0006 | 0.9769 ± 0.0001 |
| FPR | 0.0000 ± 0.0000 | 0.0167 ± 0.0008 | 0.0127 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9813 ± 0.0001 | 0.9827 ± 0.0002 |
| MCC | 1.0000 ± 0.0000 | 0.9622 ± 0.0003 | 0.9635 ± 0.0003 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 18.3 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 371 070 |
| veľkosť modelu na disku | 20.67 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.135 ms (p95 0.160) |
| CPU priepustnosť (24 vlákien) | 111 697 vzoriek/s |

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
