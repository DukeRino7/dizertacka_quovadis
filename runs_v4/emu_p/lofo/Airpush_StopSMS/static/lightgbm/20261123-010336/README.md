# static/lightgbm – beh `20261123-010336`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/static/lightgbm/20261122-231010`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.03701536655085927, "num_leaves": 240, "min_child_samples": 18, "feature_fraction": 0.860319963795015, "bagging_fraction": 0.9949001098214416, "lambda_l1": 1.0205843882460235e-07, "lambda_l2": 0.00015478320101473535}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9944 ± 0.0001 | 0.9870 ± 0.0002 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9939 ± 0.0000 | 0.9873 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9556 ± 0.0013 | 0.8710 ± 0.0002 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8714 ± 0.0118 | 0.7224 ± 0.0051 |
| log loss | 0.0010 ± 0.0002 | 0.1041 ± 0.0037 | 0.2497 ± 0.0120 |
| Brier skóre | 0.0002 ± 0.0000 | 0.0197 ± 0.0002 | 0.0492 ± 0.0009 |

Rozdiel ROC-AUC train − validácia: **0.0056** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9998 ± 0.0000 | 0.9770 ± 0.0006 | 0.9289 ± 0.0014 |
| balanced accuracy | 0.9997 ± 0.0000 | 0.9730 ± 0.0008 | 0.9215 ± 0.0016 |
| precision | 1.0000 ± 0.0000 | 0.9844 ± 0.0005 | 0.9897 ± 0.0003 |
| recall (TPR) | 0.9995 ± 0.0000 | 0.9556 ± 0.0013 | 0.8502 ± 0.0033 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0003 | 0.0072 ± 0.0002 |
| F1 | 0.9997 ± 0.0000 | 0.9698 ± 0.0008 | 0.9147 ± 0.0018 |
| MCC | 0.9996 ± 0.0000 | 0.9515 ± 0.0013 | 0.8616 ± 0.0026 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9996 ± 0.0000 | 0.9772 ± 0.0005 | 0.9423 ± 0.0005 |
| balanced accuracy | 0.9996 ± 0.0000 | 0.9753 ± 0.0005 | 0.9373 ± 0.0006 |
| precision | 0.9992 ± 0.0000 | 0.9735 ± 0.0005 | 0.9807 ± 0.0000 |
| recall (TPR) | 0.9997 ± 0.0000 | 0.9673 ± 0.0009 | 0.8887 ± 0.0012 |
| FPR | 0.0005 ± 0.0000 | 0.0166 ± 0.0003 | 0.0142 ± 0.0000 |
| F1 | 0.9995 ± 0.0000 | 0.9704 ± 0.0006 | 0.9325 ± 0.0007 |
| MCC | 0.9992 ± 0.0000 | 0.9518 ± 0.0010 | 0.8856 ± 0.0010 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 8.4 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 291 232 |
| veľkosť modelu na disku | 16.32 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.113 ms (p95 0.136) |
| CPU priepustnosť (24 vlákien) | 126 800 vzoriek/s |

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
