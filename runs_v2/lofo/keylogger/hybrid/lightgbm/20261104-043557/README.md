# hybrid/lightgbm – beh `20261104-043557`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9701 ± 0.0078 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9809 ± 0.0037 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9974 ± 0.0002 | 0.9137 ± 0.0010 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9927 ± 0.0008 | 0.8584 ± 0.0033 |
| log loss | 0.0008 ± 0.0005 | 0.0132 ± 0.0003 | 0.4327 ± 0.0317 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0034 ± 0.0002 | 0.0656 ± 0.0016 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9954 ± 0.0004 | 0.9318 ± 0.0015 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9945 ± 0.0004 | 0.9368 ± 0.0013 |
| precision | 1.0000 ± 0.0000 | 0.9955 ± 0.0003 | 0.9963 ± 0.0006 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9974 ± 0.0002 | 0.8775 ± 0.0032 |
| FPR | 0.0000 ± 0.0000 | 0.0085 ± 0.0006 | 0.0038 ± 0.0007 |
| F1 | 1.0000 ± 0.0000 | 0.9964 ± 0.0003 | 0.9331 ± 0.0016 |
| MCC | 1.0000 ± 0.0000 | 0.9897 ± 0.0008 | 0.8714 ± 0.0024 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9955 ± 0.0004 | 0.9264 ± 0.0005 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9955 ± 0.0003 | 0.9320 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9976 ± 0.0002 | 0.9984 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9955 ± 0.0005 | 0.8657 ± 0.0012 |
| FPR | 0.0000 ± 0.0000 | 0.0045 ± 0.0004 | 0.0016 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9965 ± 0.0003 | 0.9273 ± 0.0006 |
| MCC | 1.0000 ± 0.0000 | 0.9901 ± 0.0008 | 0.8625 ± 0.0009 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 14.5 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 19 614 |
| veľkosť modelu na disku | 1.16 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.038 ms (p95 0.049) |
| CPU priepustnosť (24 vlákien) | 254 643 vzoriek/s |

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
