# static/rf – beh `20261101-213728`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `random_forest` – Random Forest (pôvodné hodnoty príznakov)
- **Ladenie:** 30 dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, 14.8 min
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"n_estimators": 250, "max_depth": null, "min_samples_leaf": 1, "max_features": "sqrt"}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9990 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9999 ± 0.0000 | 0.9992 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9951 ± 0.0001 | 0.9699 ± 0.0012 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9850 ± 0.0020 | 0.9201 ± 0.0029 |
| log loss | 0.0077 ± 0.0000 | 0.0253 ± 0.0001 | 0.0929 ± 0.0014 |
| Brier skóre | 0.0010 ± 0.0000 | 0.0059 ± 0.0000 | 0.0253 ± 0.0005 |

Rozdiel ROC-AUC train − validácia: **0.0002** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9936 ± 0.0002 | 0.9765 ± 0.0006 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9928 ± 0.0003 | 0.9779 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9953 ± 0.0002 | 0.9949 ± 0.0004 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9951 ± 0.0001 | 0.9616 ± 0.0015 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0005 | 0.0058 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9952 ± 0.0002 | 0.9780 ± 0.0006 |
| MCC | 1.0000 ± 0.0000 | 0.9855 ± 0.0005 | 0.9535 ± 0.0011 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9937 ± 0.0003 | 0.9666 ± 0.0002 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9941 ± 0.0003 | 0.9690 ± 0.0002 |
| precision | 1.0000 ± 0.0000 | 0.9976 ± 0.0002 | 0.9980 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9929 ± 0.0002 | 0.9402 ± 0.0004 |
| FPR | 0.0000 ± 0.0000 | 0.0048 ± 0.0005 | 0.0023 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9953 ± 0.0002 | 0.9682 ± 0.0002 |
| MCC | 1.0000 ± 0.0000 | 0.9857 ± 0.0006 | 0.9349 ± 0.0003 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 27.4 s (priemer cez seedy) |
| ladenie spolu | 888 s |
| počet parametrov / uzlov | 390 428 |
| veľkosť modelu na disku | 31.60 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 7.312 ms (p95 7.617) |
| CPU priepustnosť (24 vlákien) | 139 848 vzoriek/s |

## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
| ![ladenie](plots/hpo_history.png) |  |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
