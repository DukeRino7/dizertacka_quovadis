# hybrid/lightgbm – beh `20261123-185825`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.156156388281821, "num_leaves": 106, "min_child_samples": 12, "feature_fraction": 0.9629001596575603, "bagging_fraction": 0.9482638746669452, "lambda_l1": 1.6337309047659264e-08, "lambda_l2": 0.01636800654484922}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9969 ± 0.0001 | 0.9965 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9970 ± 0.0001 | 0.9964 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9715 ± 0.0010 | 0.9585 ± 0.0015 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8909 ± 0.0046 | 0.8966 ± 0.0108 |
| log loss | 0.0004 ± 0.0002 | 0.0729 ± 0.0062 | 0.1001 ± 0.0089 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0152 ± 0.0002 | 0.0206 ± 0.0005 |

Rozdiel ROC-AUC train − validácia: **0.0031** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9823 ± 0.0006 | 0.9743 ± 0.0006 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9810 ± 0.0006 | 0.9722 ± 0.0006 |
| precision | 1.0000 ± 0.0000 | 0.9874 ± 0.0004 | 0.9911 ± 0.0006 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9715 ± 0.0010 | 0.9513 ± 0.0009 |
| FPR | 0.0000 ± 0.0000 | 0.0095 ± 0.0003 | 0.0070 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9794 ± 0.0007 | 0.9708 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9640 ± 0.0012 | 0.9485 ± 0.0011 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9812 ± 0.0002 | 0.9760 ± 0.0006 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9805 ± 0.0001 | 0.9743 ± 0.0007 |
| precision | 1.0000 ± 0.0000 | 0.9805 ± 0.0008 | 0.9874 ± 0.0007 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9759 ± 0.0006 | 0.9586 ± 0.0016 |
| FPR | 0.0000 ± 0.0000 | 0.0148 ± 0.0006 | 0.0100 ± 0.0006 |
| F1 | 1.0000 ± 0.0000 | 0.9782 ± 0.0002 | 0.9728 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9616 ± 0.0003 | 0.9516 ± 0.0012 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 4.1 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 35 026 |
| veľkosť modelu na disku | 1.95 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.033 ms (p95 0.041) |
| CPU priepustnosť (24 vlákien) | 620 660 vzoriek/s |

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
