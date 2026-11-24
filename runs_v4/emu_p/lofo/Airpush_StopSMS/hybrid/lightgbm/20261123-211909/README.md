# hybrid/lightgbm – beh `20261123-211909`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.021805367982090686, "num_leaves": 214, "min_child_samples": 11, "feature_fraction": 0.7934614803684483, "bagging_fraction": 0.9747297177039957, "lambda_l1": 3.6112431454858456e-05, "lambda_l2": 1.814656418208834e-05}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9967 ± 0.0001 | 0.9910 ± 0.0002 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9962 ± 0.0001 | 0.9910 ± 0.0002 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9630 ± 0.0009 | 0.9019 ± 0.0033 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9087 ± 0.0059 | 0.7884 ± 0.0104 |
| log loss | 0.0016 ± 0.0009 | 0.0640 ± 0.0033 | 0.1643 ± 0.0114 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0161 ± 0.0002 | 0.0387 ± 0.0002 |

Rozdiel ROC-AUC train − validácia: **0.0033** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9798 ± 0.0004 | 0.9437 ± 0.0011 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9767 ± 0.0005 | 0.9380 ± 0.0013 |
| precision | 1.0000 ± 0.0000 | 0.9845 ± 0.0003 | 0.9905 ± 0.0007 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9630 ± 0.0009 | 0.8829 ± 0.0030 |
| FPR | 0.0000 ± 0.0000 | 0.0096 ± 0.0002 | 0.0069 ± 0.0005 |
| F1 | 1.0000 ± 0.0000 | 0.9737 ± 0.0006 | 0.9336 ± 0.0015 |
| MCC | 1.0000 ± 0.0000 | 0.9575 ± 0.0009 | 0.8895 ± 0.0021 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9794 ± 0.0003 | 0.9518 ± 0.0004 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9776 ± 0.0003 | 0.9475 ± 0.0004 |
| precision | 1.0000 ± 0.0000 | 0.9767 ± 0.0005 | 0.9857 ± 0.0005 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9699 ± 0.0003 | 0.9056 ± 0.0004 |
| FPR | 0.0000 ± 0.0000 | 0.0146 ± 0.0003 | 0.0106 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9733 ± 0.0003 | 0.9440 ± 0.0004 |
| MCC | 1.0000 ± 0.0000 | 0.9565 ± 0.0006 | 0.9044 ± 0.0007 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 12.9 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 281 820 |
| veľkosť modelu na disku | 15.72 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.114 ms (p95 0.138) |
| CPU priepustnosť (24 vlákien) | 121 399 vzoriek/s |

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
