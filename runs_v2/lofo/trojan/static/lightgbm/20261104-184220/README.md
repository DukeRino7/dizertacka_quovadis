# static/lightgbm – beh `20261104-184220`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/static/lightgbm/20261101-215345`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.017398074711291726, "num_leaves": 461, "min_child_samples": 101, "feature_fraction": 0.9576492590949324, "bagging_fraction": 0.9474136752138245, "lambda_l1": 0.002404915432737351, "lambda_l2": 1.9809253750493907}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9989 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9991 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9970 ± 0.0001 | 0.9829 ± 0.0013 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9876 ± 0.0007 | 0.9109 ± 0.0035 |
| log loss | 0.0001 ± 0.0001 | 0.0163 ± 0.0004 | 0.1020 ± 0.0051 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0038 ± 0.0001 | 0.0239 ± 0.0005 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9951 ± 0.0003 | 0.9820 ± 0.0011 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9945 ± 0.0003 | 0.9831 ± 0.0010 |
| precision | 1.0000 ± 0.0000 | 0.9952 ± 0.0003 | 0.9970 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9970 ± 0.0001 | 0.9698 ± 0.0019 |
| FPR | 0.0000 ± 0.0000 | 0.0081 ± 0.0005 | 0.0035 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9961 ± 0.0002 | 0.9832 ± 0.0010 |
| MCC | 1.0000 ± 0.0000 | 0.9896 ± 0.0006 | 0.9643 ± 0.0021 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9948 ± 0.0003 | 0.9735 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9950 ± 0.0003 | 0.9754 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9975 ± 0.0003 | 0.9985 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9942 ± 0.0001 | 0.9525 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0042 ± 0.0005 | 0.0017 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9959 ± 0.0002 | 0.9750 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9889 ± 0.0006 | 0.9480 ± 0.0003 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 318.5 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 688 968 |
| veľkosť modelu na disku | 40.47 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.434 ms (p95 0.574) |
| CPU priepustnosť (24 vlákien) | 27 137 vzoriek/s |

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
