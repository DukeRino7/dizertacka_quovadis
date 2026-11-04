# hybrid/lightgbm – beh `20261104-063626`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lightgbm/20261102-052826`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.13394334706750485, "num_leaves": 127, "min_child_samples": 82, "feature_fraction": 0.3144091460070617, "bagging_fraction": 0.9849549260809971, "lambda_l1": 0.31044435499483225, "lambda_l2": 8.148018307012941e-07}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9994 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9995 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9964 ± 0.0009 | 0.9922 ± 0.0006 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9868 ± 0.0026 | 0.9482 ± 0.0163 |
| log loss | 0.0003 ± 0.0000 | 0.0166 ± 0.0010 | 0.0481 ± 0.0021 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0042 ± 0.0003 | 0.0124 ± 0.0007 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9942 ± 0.0006 | 0.9893 ± 0.0008 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9934 ± 0.0005 | 0.9898 ± 0.0007 |
| precision | 1.0000 ± 0.0000 | 0.9942 ± 0.0001 | 0.9965 ± 0.0008 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9964 ± 0.0009 | 0.9836 ± 0.0017 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0002 | 0.0041 ± 0.0009 |
| F1 | 1.0000 ± 0.0000 | 0.9953 ± 0.0005 | 0.9900 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9876 ± 0.0013 | 0.9785 ± 0.0015 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9946 ± 0.0002 | 0.9846 ± 0.0009 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9947 ± 0.0003 | 0.9857 ± 0.0008 |
| precision | 1.0000 ± 0.0000 | 0.9968 ± 0.0006 | 0.9985 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9945 ± 0.0004 | 0.9731 ± 0.0018 |
| FPR | 0.0000 ± 0.0000 | 0.0052 ± 0.0010 | 0.0017 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9957 ± 0.0001 | 0.9856 ± 0.0008 |
| MCC | 1.0000 ± 0.0000 | 0.9886 ± 0.0004 | 0.9695 ± 0.0017 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 16.7 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 29 188 |
| veľkosť modelu na disku | 1.64 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.095 ms (p95 0.114) |
| CPU priepustnosť (24 vlákien) | 266 298 vzoriek/s |

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
