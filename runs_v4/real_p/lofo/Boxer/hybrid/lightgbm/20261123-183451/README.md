# hybrid/lightgbm – beh `20261123-183451`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.156156388281821, "num_leaves": 106, "min_child_samples": 12, "feature_fraction": 0.9629001596575603, "bagging_fraction": 0.9482638746669452, "lambda_l1": 1.6337309047659264e-08, "lambda_l2": 0.01636800654484922}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9964 ± 0.0001 | 0.9979 ± 0.0001 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9963 ± 0.0000 | 0.9978 ± 0.0001 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9624 ± 0.0013 | 0.9683 ± 0.0033 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8748 ± 0.0047 | 0.9042 ± 0.0103 |
| log loss | 0.0005 ± 0.0003 | 0.0780 ± 0.0045 | 0.0633 ± 0.0008 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0167 ± 0.0002 | 0.0154 ± 0.0006 |

Rozdiel ROC-AUC train − validácia: **0.0036** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9790 ± 0.0004 | 0.9786 ± 0.0009 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9766 ± 0.0005 | 0.9769 ± 0.0009 |
| precision | 1.0000 ± 0.0000 | 0.9868 ± 0.0007 | 0.9914 ± 0.0011 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9624 ± 0.0013 | 0.9605 ± 0.0014 |
| FPR | 0.0000 ± 0.0000 | 0.0092 ± 0.0005 | 0.0067 ± 0.0009 |
| F1 | 1.0000 ± 0.0000 | 0.9744 ± 0.0005 | 0.9757 ± 0.0010 |
| MCC | 1.0000 ± 0.0000 | 0.9569 ± 0.0009 | 0.9570 ± 0.0017 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9798 ± 0.0006 | 0.9808 ± 0.0006 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9788 ± 0.0006 | 0.9798 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9781 ± 0.0008 | 0.9861 ± 0.0018 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9731 ± 0.0012 | 0.9708 ± 0.0007 |
| FPR | 0.0000 ± 0.0000 | 0.0155 ± 0.0006 | 0.0111 ± 0.0014 |
| F1 | 1.0000 ± 0.0000 | 0.9756 ± 0.0007 | 0.9784 ± 0.0007 |
| MCC | 1.0000 ± 0.0000 | 0.9584 ± 0.0012 | 0.9612 ± 0.0013 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 4.0 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 42 622 |
| veľkosť modelu na disku | 2.39 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.038 ms (p95 0.045) |
| CPU priepustnosť (24 vlákien) | 544 367 vzoriek/s |

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
