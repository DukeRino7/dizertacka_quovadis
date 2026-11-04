# hybrid/lr – beh `20261104-021449`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `logreg` – logistická regresia s L2 regularizáciou (vstup signed log1p + štandardizácia)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/lr/20261102-044357`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"max_iter": 2000, "C": 0.0028355883180749405}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9996 ± 0.0000 | 0.9986 ± 0.0000 | 0.9967 ± 0.0000 |
| PR-AUC | 0.9998 ± 0.0000 | 0.9976 ± 0.0000 | 0.9971 ± 0.0000 |
| TPR pri FPR 1 % | 0.9974 ± 0.0000 | 0.9870 ± 0.0000 | 0.9355 ± 0.0000 |
| TPR pri FPR 0,1 % | 0.9289 ± 0.0000 | 0.9036 ± 0.0000 | 0.6478 ± 0.0000 |
| log loss | 0.0246 ± 0.0000 | 0.0358 ± 0.0000 | 0.1008 ± 0.0000 |
| Brier skóre | 0.0052 ± 0.0000 | 0.0076 ± 0.0000 | 0.0286 ± 0.0000 |

Rozdiel ROC-AUC train − validácia: **0.0010** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9917 ± 0.0000 | 0.9883 ± 0.0000 | 0.9520 ± 0.0000 |
| balanced accuracy | 0.9924 ± 0.0000 | 0.9888 ± 0.0000 | 0.9552 ± 0.0000 |
| precision | 0.9972 ± 0.0000 | 0.9944 ± 0.0000 | 0.9946 ± 0.0000 |
| recall (TPR) | 0.9894 ± 0.0000 | 0.9870 ± 0.0000 | 0.9164 ± 0.0000 |
| FPR | 0.0045 ± 0.0000 | 0.0094 ± 0.0000 | 0.0059 ± 0.0000 |
| F1 | 0.9933 ± 0.0000 | 0.9907 ± 0.0000 | 0.9539 ± 0.0000 |
| MCC | 0.9825 ± 0.0000 | 0.9751 ± 0.0000 | 0.9072 ± 0.0000 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9953 ± 0.0000 | 0.9914 ± 0.0000 | 0.9615 ± 0.0000 |
| balanced accuracy | 0.9948 ± 0.0000 | 0.9907 ± 0.0000 | 0.9637 ± 0.0000 |
| precision | 0.9957 ± 0.0000 | 0.9930 ± 0.0000 | 0.9906 ± 0.0000 |
| recall (TPR) | 0.9968 ± 0.0000 | 0.9933 ± 0.0000 | 0.9380 ± 0.0000 |
| FPR | 0.0071 ± 0.0000 | 0.0119 ± 0.0000 | 0.0106 ± 0.0000 |
| F1 | 0.9962 ± 0.0000 | 0.9931 ± 0.0000 | 0.9635 ± 0.0000 |
| MCC | 0.9900 ± 0.0000 | 0.9815 ± 0.0000 | 0.9244 ± 0.0000 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 4.8 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 4 320 |
| veľkosť modelu na disku | 0.13 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.034 ms |
| transformácia vstupu – priepustnosť | 23 470 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.007 ms (p95 0.008) |
| CPU priepustnosť (24 vlákien) | 164 582 vzoriek/s |

## Grafy
| | |
|---|---|
| ![ROC](plots/roc.png) | ![PR](plots/pr.png) |
| ![skóre](plots/score_hist_test.png) | ![rodiny](plots/per_family.png) |
| ![matica zámen](plots/confusion_test_val_fpr.png) | ![matica zámen 0.5](plots/confusion_test_fixed.png) |
|  |  |

## Súbory
`metrics.json` (všetky metriky po seedoch vrátane rodín), `timing.json`, `hpo_trials.csv`,
`predictions/<časť>_seed<N>.parquet` (sha256, family, label, score), `model/seed_<N>/`, `log.txt`.
