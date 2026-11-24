# hybrid/lightgbm – beh `20261123-221915`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.021805367982090686, "num_leaves": 214, "min_child_samples": 11, "feature_fraction": 0.7934614803684483, "bagging_fraction": 0.9747297177039957, "lambda_l1": 3.6112431454858456e-05, "lambda_l2": 1.814656418208834e-05}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9958 ± 0.0001 | 0.9968 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9959 ± 0.0001 | 0.9970 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9569 ± 0.0009 | 0.9695 ± 0.0014 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8562 ± 0.0049 | 0.9102 ± 0.0099 |
| log loss | 0.0020 ± 0.0013 | 0.0728 ± 0.0043 | 0.0631 ± 0.0034 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0172 ± 0.0001 | 0.0153 ± 0.0001 |

Rozdiel ROC-AUC train − validácia: **0.0042** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9759 ± 0.0005 | 0.9788 ± 0.0009 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9737 ± 0.0006 | 0.9771 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9874 ± 0.0004 | 0.9916 ± 0.0005 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9569 ± 0.0009 | 0.9608 ± 0.0016 |
| FPR | 0.0000 ± 0.0000 | 0.0095 ± 0.0003 | 0.0066 ± 0.0004 |
| F1 | 1.0000 ± 0.0000 | 0.9719 ± 0.0006 | 0.9759 ± 0.0010 |
| MCC | 1.0000 ± 0.0000 | 0.9511 ± 0.0010 | 0.9573 ± 0.0017 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9785 ± 0.0004 | 0.9807 ± 0.0007 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9779 ± 0.0004 | 0.9802 ± 0.0006 |
| precision | 1.0000 ± 0.0000 | 0.9783 ± 0.0009 | 0.9825 ± 0.0013 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9724 ± 0.0006 | 0.9744 ± 0.0003 |
| FPR | 0.0000 ± 0.0000 | 0.0167 ± 0.0007 | 0.0141 ± 0.0011 |
| F1 | 1.0000 ± 0.0000 | 0.9754 ± 0.0005 | 0.9784 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9564 ± 0.0009 | 0.9611 ± 0.0013 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 14.5 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 224 175 |
| veľkosť modelu na disku | 12.43 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.090 ms (p95 0.108) |
| CPU priepustnosť (24 vlákien) | 148 078 vzoriek/s |

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
