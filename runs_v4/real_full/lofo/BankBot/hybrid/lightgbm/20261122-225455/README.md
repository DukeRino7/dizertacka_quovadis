# hybrid/lightgbm – beh `20261122-225455`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.018196998780495684, "num_leaves": 233, "min_child_samples": 23, "feature_fraction": 0.6390322800765896, "bagging_fraction": 0.9532240144545877, "lambda_l1": 0.008505404243799093, "lambda_l2": 0.007794186652208281}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9975 ± 0.0000 | 0.9983 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9982 ± 0.0000 | 0.9987 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9730 ± 0.0003 | 0.9773 ± 0.0010 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9190 ± 0.0025 | 0.9315 ± 0.0040 |
| log loss | 0.0007 ± 0.0005 | 0.0626 ± 0.0029 | 0.0537 ± 0.0025 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0145 ± 0.0001 | 0.0128 ± 0.0001 |

Rozdiel ROC-AUC train − validácia: **0.0025** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9813 ± 0.0001 | 0.9824 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9816 ± 0.0001 | 0.9830 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9909 ± 0.0001 | 0.9929 ± 0.0003 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9730 ± 0.0003 | 0.9739 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0002 | 0.0079 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9819 ± 0.0001 | 0.9833 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9627 ± 0.0003 | 0.9650 ± 0.0002 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9818 ± 0.0008 | 0.9843 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9819 ± 0.0008 | 0.9845 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9851 ± 0.0006 | 0.9890 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9800 ± 0.0010 | 0.9813 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0161 ± 0.0006 | 0.0122 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9825 ± 0.0008 | 0.9852 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9636 ± 0.0016 | 0.9686 ± 0.0002 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 21.8 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 484 995 |
| veľkosť modelu na disku | 27.08 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.173 ms (p95 0.208) |
| CPU priepustnosť (24 vlákien) | 76 914 vzoriek/s |

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
