# hybrid/lightgbm – beh `20261123-214927`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.021805367982090686, "num_leaves": 214, "min_child_samples": 11, "feature_fraction": 0.7934614803684483, "bagging_fraction": 0.9747297177039957, "lambda_l1": 3.6112431454858456e-05, "lambda_l2": 1.814656418208834e-05}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9957 ± 0.0001 | 0.9966 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9958 ± 0.0001 | 0.9968 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9598 ± 0.0009 | 0.9637 ± 0.0019 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8582 ± 0.0044 | 0.8915 ± 0.0083 |
| log loss | 0.0018 ± 0.0008 | 0.0723 ± 0.0014 | 0.0661 ± 0.0017 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0170 ± 0.0003 | 0.0162 ± 0.0001 |

Rozdiel ROC-AUC train − validácia: **0.0043** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9772 ± 0.0004 | 0.9768 ± 0.0005 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9750 ± 0.0004 | 0.9750 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9867 ± 0.0000 | 0.9912 ± 0.0005 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9598 ± 0.0009 | 0.9568 ± 0.0006 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0000 | 0.0069 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9731 ± 0.0005 | 0.9737 ± 0.0005 |
| MCC | 1.0000 ± 0.0000 | 0.9536 ± 0.0008 | 0.9535 ± 0.0010 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9791 ± 0.0009 | 0.9793 ± 0.0006 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9781 ± 0.0009 | 0.9785 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9794 ± 0.0014 | 0.9824 ± 0.0008 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9717 ± 0.0012 | 0.9713 ± 0.0005 |
| FPR | 0.0000 ± 0.0000 | 0.0154 ± 0.0011 | 0.0142 ± 0.0007 |
| F1 | 1.0000 ± 0.0000 | 0.9755 ± 0.0011 | 0.9768 ± 0.0006 |
| MCC | 1.0000 ± 0.0000 | 0.9572 ± 0.0019 | 0.9582 ± 0.0011 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 13.8 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 241 255 |
| veľkosť modelu na disku | 13.39 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.099 ms (p95 0.118) |
| CPU priepustnosť (24 vlákien) | 139 956 vzoriek/s |

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
