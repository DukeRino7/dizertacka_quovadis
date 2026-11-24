# dynamic/lr – beh `20261123-184342`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `logreg` – logistická regresia s L2 regularizáciou (vstup signed log1p + štandardizácia)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/dynamic/lr/20261122-233312`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"max_iter": 2000, "C": 9.535095002298556}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9209 ± 0.0000 | 0.9126 ± 0.0000 | 0.9137 ± 0.0000 |
| PR-AUC | 0.9183 ± 0.0000 | 0.9146 ± 0.0000 | 0.9189 ± 0.0000 |
| TPR pri FPR 1 % | 0.5360 ± 0.0000 | 0.5437 ± 0.0000 | 0.5392 ± 0.0000 |
| TPR pri FPR 0,1 % | 0.4065 ± 0.0000 | 0.4007 ± 0.0000 | 0.3878 ± 0.0000 |
| log loss | 0.3434 ± 0.0000 | 0.3558 ± 0.0000 | 0.3600 ± 0.0000 |
| Brier skóre | 0.1054 ± 0.0000 | 0.1094 ± 0.0000 | 0.1100 ± 0.0000 |

Rozdiel ROC-AUC train − validácia: **0.0083** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.8085 ± 0.0000 | 0.7986 ± 0.0000 | 0.7822 ± 0.0000 |
| balanced accuracy | 0.7748 ± 0.0000 | 0.7670 ± 0.0000 | 0.7581 ± 0.0000 |
| precision | 0.9712 ± 0.0000 | 0.9767 ± 0.0000 | 0.9809 ± 0.0000 |
| recall (TPR) | 0.5617 ± 0.0000 | 0.5437 ± 0.0000 | 0.5244 ± 0.0000 |
| FPR | 0.0121 ± 0.0000 | 0.0097 ± 0.0000 | 0.0083 ± 0.0000 |
| F1 | 0.7117 ± 0.0000 | 0.6985 ± 0.0000 | 0.6834 ± 0.0000 |
| MCC | 0.6323 ± 0.0000 | 0.6198 ± 0.0000 | 0.6013 ± 0.0000 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.8599 ± 0.0000 | 0.8503 ± 0.0000 | 0.8512 ± 0.0000 |
| balanced accuracy | 0.8538 ± 0.0000 | 0.8437 ± 0.0000 | 0.8463 ± 0.0000 |
| precision | 0.8463 ± 0.0000 | 0.8455 ± 0.0000 | 0.8592 ± 0.0000 |
| recall (TPR) | 0.8152 ± 0.0000 | 0.7968 ± 0.0000 | 0.7990 ± 0.0000 |
| FPR | 0.1076 ± 0.0000 | 0.1095 ± 0.0000 | 0.1064 ± 0.0000 |
| F1 | 0.8304 ± 0.0000 | 0.8204 ± 0.0000 | 0.8280 ± 0.0000 |
| MCC | 0.7115 ± 0.0000 | 0.6932 ± 0.0000 | 0.6986 ± 0.0000 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 0.3 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 124 |
| veľkosť modelu na disku | 0.01 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.005 ms |
| transformácia vstupu – priepustnosť | 1 370 617 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.004 ms (p95 0.004) |
| CPU priepustnosť (24 vlákien) | 3 873 772 vzoriek/s |

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
