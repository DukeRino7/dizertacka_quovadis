# static/lightgbm – beh `20261104-012654`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/static/lightgbm/20261101-215345`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.017398074711291726, "num_leaves": 461, "min_child_samples": 101, "feature_fraction": 0.9576492590949324, "bagging_fraction": 0.9474136752138245, "lambda_l1": 0.002404915432737351, "lambda_l2": 1.9809253750493907}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9995 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9996 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9976 ± 0.0004 | 0.9921 ± 0.0022 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9897 ± 0.0013 | 0.9638 ± 0.0011 |
| log loss | 0.0003 ± 0.0003 | 0.0144 ± 0.0002 | 0.0448 ± 0.0007 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0036 ± 0.0002 | 0.0120 ± 0.0002 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9949 ± 0.0002 | 0.9886 ± 0.0017 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9940 ± 0.0001 | 0.9891 ± 0.0016 |
| precision | 1.0000 ± 0.0000 | 0.9943 ± 0.0001 | 0.9960 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9976 ± 0.0004 | 0.9829 ± 0.0034 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0002 | 0.0047 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9960 ± 0.0001 | 0.9894 ± 0.0016 |
| MCC | 1.0000 ± 0.0000 | 0.9891 ± 0.0004 | 0.9772 ± 0.0034 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9953 ± 0.0004 | 0.9843 ± 0.0010 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9951 ± 0.0005 | 0.9853 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9966 ± 0.0004 | 0.9980 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9959 ± 0.0002 | 0.9729 ± 0.0016 |
| FPR | 0.0000 ± 0.0000 | 0.0057 ± 0.0007 | 0.0023 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9963 ± 0.0003 | 0.9853 ± 0.0009 |
| MCC | 1.0000 ± 0.0000 | 0.9899 ± 0.0009 | 0.9688 ± 0.0019 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 220.2 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 497 386 |
| veľkosť modelu na disku | 29.17 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.303 ms (p95 0.398) |
| CPU priepustnosť (24 vlákien) | 40 926 vzoriek/s |

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
