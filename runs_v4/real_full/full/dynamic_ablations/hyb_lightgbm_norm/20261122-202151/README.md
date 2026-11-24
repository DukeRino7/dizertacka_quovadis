# hybrid_norm/hyb_lightgbm_norm – beh `20261122-202151`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – hybrid lightgbm s dynamikou ako podiely systémových volaní (kontrola artefaktu množstva aktivity)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.018196998780495684, "num_leaves": 233, "min_child_samples": 23, "feature_fraction": 0.6390322800765896, "bagging_fraction": 0.9532240144545877, "lambda_l1": 0.008505404243799093, "lambda_l2": 0.007794186652208281}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9971 ± 0.0000 | 0.9980 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9979 ± 0.0000 | 0.9985 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9696 ± 0.0006 | 0.9777 ± 0.0005 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8999 ± 0.0020 | 0.9210 ± 0.0019 |
| log loss | 0.0008 ± 0.0001 | 0.0671 ± 0.0011 | 0.0558 ± 0.0005 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0159 ± 0.0001 | 0.0133 ± 0.0000 |

Rozdiel ROC-AUC train − validácia: **0.0029** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9794 ± 0.0003 | 0.9810 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9800 ± 0.0002 | 0.9817 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9912 ± 0.0001 | 0.9939 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9696 ± 0.0006 | 0.9701 ± 0.0001 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0002 | 0.0068 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9803 ± 0.0003 | 0.9818 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9589 ± 0.0005 | 0.9622 ± 0.0001 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9795 ± 0.0003 | 0.9836 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9795 ± 0.0003 | 0.9838 ± 0.0001 |
| precision | 1.0000 ± 0.0000 | 0.9828 ± 0.0002 | 0.9889 ± 0.0004 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9784 ± 0.0004 | 0.9799 ± 0.0001 |
| FPR | 0.0000 ± 0.0000 | 0.0193 ± 0.0003 | 0.0123 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9806 ± 0.0003 | 0.9844 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9588 ± 0.0005 | 0.9671 ± 0.0003 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 26.1 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 377 580 |
| veľkosť modelu na disku | 21.29 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.134 ms (p95 0.159) |
| CPU priepustnosť (24 vlákien) | 111 422 vzoriek/s |

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
