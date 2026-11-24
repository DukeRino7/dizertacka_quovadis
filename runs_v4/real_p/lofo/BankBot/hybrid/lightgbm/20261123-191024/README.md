# hybrid/lightgbm – beh `20261123-191024`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/hybrid/lightgbm/20261122-235912`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.156156388281821, "num_leaves": 106, "min_child_samples": 12, "feature_fraction": 0.9629001596575603, "bagging_fraction": 0.9482638746669452, "lambda_l1": 1.6337309047659264e-08, "lambda_l2": 0.01636800654484922}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9967 ± 0.0001 | 0.9982 ± 0.0000 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9969 ± 0.0001 | 0.9982 ± 0.0000 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9699 ± 0.0015 | 0.9774 ± 0.0012 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8676 ± 0.0205 | 0.9226 ± 0.0037 |
| log loss | 0.0001 ± 0.0001 | 0.0810 ± 0.0036 | 0.0600 ± 0.0038 |
| Brier skóre | 0.0000 ± 0.0000 | 0.0154 ± 0.0005 | 0.0128 ± 0.0003 |

Rozdiel ROC-AUC train − validácia: **0.0033** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9815 ± 0.0007 | 0.9839 ± 0.0007 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9802 ± 0.0008 | 0.9828 ± 0.0008 |
| precision | 1.0000 ± 0.0000 | 0.9876 ± 0.0000 | 0.9912 ± 0.0002 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9699 ± 0.0015 | 0.9726 ± 0.0017 |
| FPR | 0.0000 ± 0.0000 | 0.0095 ± 0.0000 | 0.0070 ± 0.0001 |
| F1 | 1.0000 ± 0.0000 | 0.9786 ± 0.0008 | 0.9818 ± 0.0008 |
| MCC | 1.0000 ± 0.0000 | 0.9625 ± 0.0014 | 0.9674 ± 0.0015 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 1.0000 ± 0.0000 | 0.9813 ± 0.0011 | 0.9845 ± 0.0005 |
| balanced accuracy | 1.0000 ± 0.0000 | 0.9807 ± 0.0011 | 0.9839 ± 0.0005 |
| precision | 1.0000 ± 0.0000 | 0.9811 ± 0.0017 | 0.9872 ± 0.0006 |
| recall (TPR) | 1.0000 ± 0.0000 | 0.9760 ± 0.0010 | 0.9781 ± 0.0006 |
| FPR | 0.0000 ± 0.0000 | 0.0146 ± 0.0013 | 0.0103 ± 0.0005 |
| F1 | 1.0000 ± 0.0000 | 0.9785 ± 0.0013 | 0.9826 ± 0.0006 |
| MCC | 1.0000 ± 0.0000 | 0.9620 ± 0.0023 | 0.9687 ± 0.0010 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 4.8 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 60 346 |
| veľkosť modelu na disku | 3.42 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.045 ms (p95 0.056) |
| CPU priepustnosť (24 vlákien) | 277 016 vzoriek/s |

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
