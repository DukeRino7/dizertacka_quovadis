# static/lightgbm – beh `20261123-185406`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `lightgbm` – LightGBM, gradient boosting stromov s early stopping na validácii (pôvodné hodnoty príznakov)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v4/real_p/full/static/lightgbm/20261122-231010`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"num_boost_round": 5000, "early_stopping_rounds": 100, "learning_rate": 0.03701536655085927, "num_leaves": 240, "min_child_samples": 18, "feature_fraction": 0.860319963795015, "bagging_fraction": 0.9949001098214416, "lambda_l1": 1.0205843882460235e-07, "lambda_l2": 0.00015478320101473535}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9942 ± 0.0001 | 0.9895 ± 0.0003 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9941 ± 0.0001 | 0.9903 ± 0.0002 |
| TPR pri FPR 1 % | 1.0000 ± 0.0000 | 0.9451 ± 0.0031 | 0.9258 ± 0.0016 |
| TPR pri FPR 0,1 % | 1.0000 ± 0.0000 | 0.8569 ± 0.0080 | 0.8414 ± 0.0099 |
| log loss | 0.0038 ± 0.0029 | 0.1054 ± 0.0227 | 0.1550 ± 0.0376 |
| Brier skóre | 0.0004 ± 0.0002 | 0.0222 ± 0.0005 | 0.0306 ± 0.0008 |

Rozdiel ROC-AUC train − validácia: **0.0058** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9976 ± 0.0019 | 0.9707 ± 0.0014 | 0.9582 ± 0.0014 |
| balanced accuracy | 0.9971 ± 0.0022 | 0.9677 ± 0.0016 | 0.9542 ± 0.0015 |
| precision | 1.0000 ± 0.0000 | 0.9867 ± 0.0000 | 0.9906 ± 0.0003 |
| recall (TPR) | 0.9943 ± 0.0044 | 0.9451 ± 0.0031 | 0.9154 ± 0.0028 |
| FPR | 0.0000 ± 0.0000 | 0.0097 ± 0.0000 | 0.0071 ± 0.0002 |
| F1 | 0.9971 ± 0.0022 | 0.9654 ± 0.0017 | 0.9515 ± 0.0017 |
| MCC | 0.9950 ± 0.0038 | 0.9407 ± 0.0027 | 0.9170 ± 0.0027 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9997 ± 0.0001 | 0.9745 ± 0.0003 | 0.9649 ± 0.0007 |
| balanced accuracy | 0.9997 ± 0.0001 | 0.9737 ± 0.0003 | 0.9628 ± 0.0009 |
| precision | 0.9995 ± 0.0000 | 0.9734 ± 0.0010 | 0.9784 ± 0.0005 |
| recall (TPR) | 0.9998 ± 0.0001 | 0.9675 ± 0.0009 | 0.9425 ± 0.0021 |
| FPR | 0.0003 ± 0.0000 | 0.0202 ± 0.0008 | 0.0169 ± 0.0004 |
| F1 | 0.9997 ± 0.0001 | 0.9705 ± 0.0003 | 0.9601 ± 0.0009 |
| MCC | 0.9995 ± 0.0001 | 0.9480 ± 0.0006 | 0.9293 ± 0.0014 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 8.3 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 210 281 |
| veľkosť modelu na disku | 11.68 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.081 ms (p95 0.095) |
| CPU priepustnosť (24 vlákien) | 163 133 vzoriek/s |

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
