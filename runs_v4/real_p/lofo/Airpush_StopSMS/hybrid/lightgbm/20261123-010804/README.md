# hybrid/lightgbm – beh `20261123-010804`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.156156388281821, "num_leaves": 106, "min_child_samples": 12, "feature_fraction": 0.9629001596575603, "bagging_fraction": 0.9482638746669452, "lambda_l1": 1.6337309047659264e-08, "lambda_l2": 0.01636800654484922}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9972 ± 0.0001 | 0.9963 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9968 ± 0.0002 | 0.9963 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9735 ± 0.0007 | 0.9551 ± 0.0034 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9220 ± 0.0048 | 0.9022 ± 0.0052 |
| log loss | 0.0006 ± 0.0008 | 0.0676 ± 0.0061 | 0.1017 ± 0.0122 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0143 ± 0.0000 | 0.0213 ± 0.0001 |

Rozdiel ROC-AUC train − validácia: **0.0028** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9841 ± 0.0005 | 0.9727 ± 0.0003 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9822 ± 0.0005 | 0.9705 ± 0.0004 |
| precision | 1.0000 ± 0.0000 | 0.9853 ± 0.0009 | 0.9899 ± 0.0010 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9735 ± 0.0007 | 0.9489 ± 0.0013 |
| FPR | 0.0000 ± 0.0000 | 0.0092 ± 0.0006 | 0.0079 ± 0.0008 |
| F1 | 1.0000 ± 0.0000 | 0.9794 ± 0.0007 | 0.9689 ± 0.0004 |
| MCC | 1.0000 ± 0.0000 | 0.9665 ± 0.0011 | 0.9453 ± 0.0007 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9830 ± 0.0004 | 0.9742 ± 0.0007 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9816 ± 0.0004 | 0.9724 ± 0.0006 |
| precision | 1.0000 ± 0.0000 | 0.9802 ± 0.0003 | 0.9874 ± 0.0014 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9756 ± 0.0007 | 0.9547 ± 0.0002 |
| FPR | 0.0000 ± 0.0000 | 0.0124 ± 0.0002 | 0.0099 ± 0.0011 |
| F1 | 1.0000 ± 0.0000 | 0.9779 ± 0.0005 | 0.9708 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9640 ± 0.0007 | 0.9482 ± 0.0014 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 3.7 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 42 411 |
| veľkosť modelu na disku | 2.38 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.037 ms (p95 0.045) |
| CPU priepustnosť (24 vlákien) | 573 482 vzoriek/s |

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
