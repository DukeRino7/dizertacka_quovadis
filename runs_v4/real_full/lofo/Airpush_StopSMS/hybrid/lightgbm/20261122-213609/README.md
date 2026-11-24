# hybrid/lightgbm – beh `20261122-213609`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_full/full/hybrid/lightgbm/20261122-195127`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.018196998780495684, "num_leaves": 233, "min_child_samples": 23, "feature_fraction": 0.6390322800765896, "bagging_fraction": 0.9532240144545877, "lambda_l1": 0.008505404243799093, "lambda_l2": 0.007794186652208281}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9976 ± 0.0000 | 0.9971 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9979 ± 0.0000 | 0.9978 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9737 ± 0.0003 | 0.9635 ± 0.0007 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.9227 ± 0.0057 | 0.9134 ± 0.0022 |
| log loss | 0.0015 ± 0.0010 | 0.0578 ± 0.0033 | 0.0793 ± 0.0054 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0140 ± 0.0002 | 0.0194 ± 0.0002 |

Rozdiel ROC-AUC train − validácia: **0.0024** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9828 ± 0.0005 | 0.9731 ± 0.0001 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9824 ± 0.0005 | 0.9741 ± 0.0000 |
| precision | 1.0000 ± 0.0000 | 0.9901 ± 0.0008 | 0.9931 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9737 ± 0.0003 | 0.9558 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0089 ± 0.0007 | 0.0075 ± 0.0002 |
| F1 | 1.0000 ± 0.0000 | 0.9819 ± 0.0005 | 0.9741 ± 0.0001 |
| MCC | 1.0000 ± 0.0000 | 0.9656 ± 0.0010 | 0.9468 ± 0.0001 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9824 ± 0.0009 | 0.9763 ± 0.0002 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9823 ± 0.0009 | 0.9770 ± 0.0002 |
| precision | 1.0000 ± 0.0000 | 0.9835 ± 0.0012 | 0.9900 ± 0.0001 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9797 ± 0.0006 | 0.9650 ± 0.0004 |
| FPR | 0.0000 ± 0.0000 | 0.0151 ± 0.0011 | 0.0110 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9816 ± 0.0009 | 0.9773 ± 0.0002 |
| MCC | 1.0000 ± 0.0000 | 0.9648 ± 0.0017 | 0.9528 ± 0.0005 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 16.4 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 398 970 |
| veľkosť modelu na disku | 22.27 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.144 ms (p95 0.176) |
| CPU priepustnosť (24 vlákien) | 107 039 vzoriek/s |

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
