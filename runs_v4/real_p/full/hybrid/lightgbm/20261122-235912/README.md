# hybrid/lightgbm – beh `20261122-235912`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** 30 dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, 5.7 min
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.156156388281821, "num_leaves": 106, "min_child_samples": 12, "feature_fraction": 0.9629001596575603, "bagging_fraction": 0.9482638746669452, "lambda_l1": 1.6337309047659264e-08, "lambda_l2": 0.01636800654484922}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9969 ± 0.0000 | 0.9982 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9972 ± 0.0000 | 0.9982 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9707 ± 0.0007 | 0.9783 ± 0.0012 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8957 ± 0.0046 | 0.9274 ± 0.0014 |
| log loss | 0.0001 ± 0.0001 | 0.0807 ± 0.0089 | 0.0604 ± 0.0059 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0154 ± 0.0001 | 0.0126 ± 0.0003 |

Rozdiel ROC-AUC train − validácia: **0.0031** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9816 ± 0.0004 | 0.9835 ± 0.0003 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9805 ± 0.0004 | 0.9824 ± 0.0004 |
| precision | 1.0000 ± 0.0000 | 0.9879 ± 0.0002 | 0.9922 ± 0.0004 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9707 ± 0.0007 | 0.9709 ± 0.0006 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0002 | 0.0062 ± 0.0003 |
| F1 | 1.0000 ± 0.0000 | 0.9792 ± 0.0005 | 0.9814 ± 0.0004 |
| MCC | 1.0000 ± 0.0000 | 0.9628 ± 0.0008 | 0.9668 ± 0.0007 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9818 ± 0.0008 | 0.9848 ± 0.0005 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9814 ± 0.0008 | 0.9842 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9824 ± 0.0008 | 0.9880 ± 0.0008 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9770 ± 0.0011 | 0.9781 ± 0.0005 |
| FPR | 0.0000 ± 0.0000 | 0.0142 ± 0.0007 | 0.0097 ± 0.0007 |
| F1 | 1.0000 ± 0.0000 | 0.9797 ± 0.0009 | 0.9830 ± 0.0006 |
| MCC | 1.0000 ± 0.0000 | 0.9632 ± 0.0016 | 0.9693 ± 0.0011 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 5.5 s (priemer cez seedy) |
| ladenie spolu | 340 s |
| počet parametrov / uzlov | 71 318 |
| veľkosť modelu na disku | 4.06 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.051 ms (p95 0.061) |
| CPU priepustnosť (24 vlákien) | 238 509 vzoriek/s |

## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
| ![ladenie](plots/hpo_history.png) | ![učenie](plots/learning_curve.png) |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
