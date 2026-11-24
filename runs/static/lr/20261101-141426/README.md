# static/lr – beh `20261101-141426`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `logreg` – logistická regresia s L2 regularizáciou (vstup signed log1p + štandardizácia)
- **Ladenie:** 30 dokončených pokusov (Optuna TPE), cieľ ROC-AUC na validácii, 3.2 min
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"max_iter": 2000, "C": 0.00515917154582608}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9996 ± 0.0000 | 0.9986 ± 0.0000 | 0.9966 ± 0.0000 |
| PR-AUC | 0.9998 ± 0.0000 | 0.9980 ± 0.0000 | 0.9938 ± 0.0000 |
| TPR pri FPR 1 % | 0.9909 ± 0.0000 | 0.9841 ± 0.0000 | 0.9675 ± 0.0000 |
| TPR pri FPR 0,1 % | 0.9369 ± 0.0000 | 0.8268 ± 0.0000 | 0.0764 ± 0.0000 |
| log loss | 0.0289 ± 0.0000 | 0.0398 ± 0.0000 | 0.0650 ± 0.0000 |
| Brier skóre | 0.0066 ± 0.0000 | 0.0094 ± 0.0000 | 0.0150 ± 0.0000 |

Rozdiel ROC-AUC train − validácia: **0.0010** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9879 ± 0.0000 | 0.9861 ± 0.0000 | 0.9714 ± 0.0000 |
| balanced accuracy | 0.9898 ± 0.0000 | 0.9872 ± 0.0000 | 0.9729 ± 0.0000 |
| precision | 0.9977 ± 0.0000 | 0.9951 ± 0.0000 | 0.9923 ± 0.0000 |
| recall (TPR) | 0.9841 ± 0.0000 | 0.9841 ± 0.0000 | 0.9547 ± 0.0000 |
| FPR | 0.0045 ± 0.0000 | 0.0098 ± 0.0000 | 0.0088 ± 0.0000 |
| F1 | 0.9909 ± 0.0000 | 0.9896 ± 0.0000 | 0.9731 ± 0.0000 |
| MCC | 0.9732 ± 0.0000 | 0.9689 ± 0.0000 | 0.9434 ± 0.0000 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9909 ± 0.0000 | 0.9868 ± 0.0000 | 0.9804 ± 0.0000 |
| balanced accuracy | 0.9912 ± 0.0000 | 0.9851 ± 0.0000 | 0.9809 ± 0.0000 |
| precision | 0.9961 ± 0.0000 | 0.9902 ± 0.0000 | 0.9877 ± 0.0000 |
| recall (TPR) | 0.9903 ± 0.0000 | 0.9902 ± 0.0000 | 0.9761 ± 0.0000 |
| FPR | 0.0078 ± 0.0000 | 0.0201 ± 0.0000 | 0.0144 ± 0.0000 |
| F1 | 0.9932 ± 0.0000 | 0.9902 ± 0.0000 | 0.9819 ± 0.0000 |
| MCC | 0.9796 ± 0.0000 | 0.9701 ± 0.0000 | 0.9607 ± 0.0000 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 6.0 s (priemer cez seedy) |
| ladenie spolu | 195 s |
| počet parametrov / uzlov | 2 320 |
| veľkosť modelu na disku | 0.05 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.050 ms |
| transformácia vstupu – priepustnosť | 15 435 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.012 ms (p95 0.013) |
| CPU priepustnosť (12 vlákien) | 193 084 vzoriek/s |

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
