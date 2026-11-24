# hybrid/rf – beh `20261123-214918`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `random_forest` – Random Forest (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/emu_p/full/hybrid/rf/20261123-195313`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"n_estimators": 200, "max_depth": null, "min_samples_leaf": 1, "max_features": "sqrt"}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9944 ± 0.0001 | 0.9950 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9943 ± 0.0001 | 0.9951 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9434 ± 0.0019 | 0.9447 ± 0.0035 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8150 ± 0.0168 | 0.8583 ± 0.0120 |
| log loss | 0.0306 ± 0.0001 | 0.1065 ± 0.0006 | 0.1116 ± 0.0020 |
| Brier skóre | 0.0034 ± 0.0000 | 0.0252 ± 0.0002 | 0.0271 ± 0.0003 |

Rozdiel ROC-AUC train − validácia: **0.0056** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9702 ± 0.0008 | 0.9655 ± 0.0004 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9669 ± 0.0009 | 0.9623 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9864 ± 0.0000 | 0.9906 ± 0.0005 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9434 ± 0.0019 | 0.9318 ± 0.0013 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0000 | 0.0072 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9645 ± 0.0010 | 0.9603 ± 0.0005 |
| MCC | 1.0000 ± 0.0000 | 0.9395 ± 0.0016 | 0.9312 ± 0.0007 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9736 ± 0.0007 | 0.9723 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9725 ± 0.0007 | 0.9708 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9736 ± 0.0015 | 0.9811 ± 0.0010 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9647 ± 0.0012 | 0.9565 ± 0.0008 |
| FPR | 0.0000 ± 0.0000 | 0.0197 ± 0.0012 | 0.0149 ± 0.0008 |
| F1 | 1.0000 ± 0.0000 | 0.9691 ± 0.0008 | 0.9687 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9461 ± 0.0014 | 0.9440 ± 0.0003 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 1.4 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 983 180 |
| veľkosť modelu na disku | 78.91 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 5.862 ms (p95 6.183) |
| CPU priepustnosť (24 vlákien) | 170 057 vzoriek/s |

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
