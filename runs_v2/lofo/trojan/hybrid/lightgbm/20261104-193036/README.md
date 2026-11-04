# hybrid/lightgbm – beh `20261104-193036`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9997 ± 0.0000 | 0.9989 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9991 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9959 ± 0.0007 | 0.9822 ± 0.0013 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9907 ± 0.0007 | 0.9131 ± 0.0240 |
| log loss | 0.0004 ± 0.0002 | 0.0167 ± 0.0001 | 0.0928 ± 0.0046 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0041 ± 0.0001 | 0.0229 ± 0.0022 |

Rozdiel ROC-AUC train − validácia: **0.0003** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9940 ± 0.0002 | 0.9819 ± 0.0015 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9934 ± 0.0003 | 0.9830 ± 0.0013 |
| precision | 1.0000 ± 0.0000 | 0.9946 ± 0.0007 | 0.9964 ± 0.0007 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9959 ± 0.0007 | 0.9702 ± 0.0032 |
| FPR | 0.0000 ± 0.0000 | 0.0091 ± 0.0012 | 0.0042 ± 0.0008 |
| F1 | 1.0000 ± 0.0000 | 0.9952 ± 0.0002 | 0.9831 ± 0.0014 |
| MCC | 1.0000 ± 0.0000 | 0.9872 ± 0.0005 | 0.9641 ± 0.0028 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9951 ± 0.0005 | 0.9720 ± 0.0063 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9952 ± 0.0005 | 0.9741 ± 0.0058 |
| precision | 1.0000 ± 0.0000 | 0.9976 ± 0.0005 | 0.9986 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9946 ± 0.0006 | 0.9497 ± 0.0116 |
| FPR | 0.0000 ± 0.0000 | 0.0041 ± 0.0008 | 0.0016 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9961 ± 0.0004 | 0.9735 ± 0.0061 |
| MCC | 1.0000 ± 0.0000 | 0.9895 ± 0.0010 | 0.9453 ± 0.0119 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 15.4 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 25 973 |
| veľkosť modelu na disku | 1.48 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.040 ms (p95 0.049) |
| CPU priepustnosť (24 vlákien) | 237 086 vzoriek/s |

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
