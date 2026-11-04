# static/mlp_kd_twobranch – beh `20261104-183737`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `mlp` – študent – malé MLP učené destiláciou z dvojvetvovej siete (V2)
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_v2/full/students_static/mlp_kd_twobranch/20261103-210128`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"hidden_layers": 1, "max_epochs": 100, "patience": 8, "hidden_width": 32, "dropout": 0.11907530604839062, "lr": 0.0013122016832935236, "weight_decay": 1.6321051677063922e-05, "batch_size": 256, "kd_alpha": 0.8749635763069835, "kd_temperature": 3.9893325789148495}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9998 ± 0.0001 | 0.9991 ± 0.0001 | 0.9972 ± 0.0001 |
| PR-AUC | 0.9999 ± 0.0000 | 0.9986 ± 0.0001 | 0.9950 ± 0.0004 |
| TPR pri FPR 1 % | 0.9959 ± 0.0022 | 0.9886 ± 0.0011 | 0.9674 ± 0.0012 |
| TPR pri FPR 0,1 % | 0.9786 ± 0.0050 | 0.9529 ± 0.0061 | 0.3768 ± 0.0797 |
| log loss | 0.0164 ± 0.0027 | 0.0274 ± 0.0012 | 0.0612 ± 0.0021 |
| Brier skóre | 0.0044 ± 0.0006 | 0.0071 ± 0.0004 | 0.0147 ± 0.0010 |

Rozdiel ROC-AUC train − validácia: **0.0007** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9929 ± 0.0007 | 0.9893 ± 0.0009 | 0.9715 ± 0.0003 |
| balanced accuracy | 0.9936 ± 0.0006 | 0.9895 ± 0.0008 | 0.9731 ± 0.0002 |
| precision | 0.9978 ± 0.0002 | 0.9951 ± 0.0002 | 0.9932 ± 0.0004 |
| recall (TPR) | 0.9914 ± 0.0011 | 0.9886 ± 0.0011 | 0.9539 ± 0.0010 |
| FPR | 0.0042 ± 0.0003 | 0.0096 ± 0.0005 | 0.0078 ± 0.0005 |
| F1 | 0.9946 ± 0.0006 | 0.9919 ± 0.0007 | 0.9732 ± 0.0003 |
| MCC | 0.9843 ± 0.0016 | 0.9761 ± 0.0020 | 0.9436 ± 0.0005 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9940 ± 0.0014 | 0.9907 ± 0.0016 | 0.9803 ± 0.0029 |
| balanced accuracy | 0.9932 ± 0.0013 | 0.9895 ± 0.0013 | 0.9809 ± 0.0027 |
| precision | 0.9952 ± 0.0004 | 0.9928 ± 0.0003 | 0.9899 ± 0.0004 |
| recall (TPR) | 0.9956 ± 0.0019 | 0.9931 ± 0.0022 | 0.9736 ± 0.0051 |
| FPR | 0.0093 ± 0.0007 | 0.0142 ± 0.0005 | 0.0118 ± 0.0004 |
| F1 | 0.9954 ± 0.0011 | 0.9930 ± 0.0012 | 0.9817 ± 0.0027 |
| MCC | 0.9866 ± 0.0032 | 0.9791 ± 0.0035 | 0.9605 ± 0.0057 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 6.6 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 74 337 |
| veľkosť modelu na disku | 0.36 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.042 ms |
| transformácia vstupu – priepustnosť | 38 504 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.068 ms (p95 0.078) |
| CPU priepustnosť (24 vlákien) | 109 150 vzoriek/s |
| GPU latencia (batch 1) | 0.287 ms (p95 0.355) |
| GPU priepustnosť | 75 269 vzoriek/s |
| GPU špičková pamäť | 1528 MB |

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
