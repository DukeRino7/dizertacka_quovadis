# hybrid/lightgbm – beh `20261104-022110`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9994 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9995 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9973 ± 0.0001 | 0.9918 ± 0.0020 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9896 ± 0.0026 | 0.9436 ± 0.0182 |
| log loss | 0.0004 ± 0.0002 | 0.0140 ± 0.0003 | 0.0531 ± 0.0096 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0035 ± 0.0002 | 0.0144 ± 0.0032 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9947 ± 0.0002 | 0.9896 ± 0.0008 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9939 ± 0.0002 | 0.9900 ± 0.0006 |
| precision | 1.0000 ± 0.0000 | 0.9944 ± 0.0001 | 0.9960 ± 0.0009 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9973 ± 0.0001 | 0.9848 ± 0.0022 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0002 | 0.0047 ± 0.0010 |
| F1 | 1.0000 ± 0.0000 | 0.9958 ± 0.0001 | 0.9904 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9887 ± 0.0004 | 0.9792 ± 0.0015 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9955 ± 0.0003 | 0.9804 ± 0.0068 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9955 ± 0.0003 | 0.9818 ± 0.0063 |
| precision | 1.0000 ± 0.0000 | 0.9974 ± 0.0001 | 0.9981 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9954 ± 0.0004 | 0.9658 ± 0.0126 |
| FPR | 0.0000 ± 0.0000 | 0.0044 ± 0.0002 | 0.0022 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9964 ± 0.0003 | 0.9816 ± 0.0066 |
| MCC | 1.0000 ± 0.0000 | 0.9904 ± 0.0007 | 0.9614 ± 0.0132 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 17.7 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 24 787 |
| veľkosť modelu na disku | 1.42 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.041 ms (p95 0.088) |
| CPU priepustnosť (24 vlákien) | 317 172 vzoriek/s |

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
