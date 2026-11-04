# static/mlp_large – beh `20261104-081259`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `mlp` – veľká neurónová sieť (3–5 skrytých vrstiev, 512–2048 neurónov), kandidát na učiteľa
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/static/mlp_large/20261101-235239`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"max_epochs": 100, "patience": 8, "hidden_layers": 5, "hidden_width": 512, "width_decay": 0.5, "dropout": 0.4556986332296347, "lr": 0.00015070674125138616, "weight_decay": 0.0036646034219705954, "batch_size": 1024}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9999 ± 0.0000 | 0.9996 ± 0.0001 | 0.9984 ± 0.0000 |
| PR-AUC | 0.9999 ± 0.0000 | 0.9998 ± 0.0001 | 0.9988 ± 0.0001 |
| TPR pri FPR 1 % | 0.9988 ± 0.0002 | 0.9949 ± 0.0003 | 0.9841 ± 0.0048 |
| TPR pri FPR 0,1 % | 0.9929 ± 0.0014 | 0.9758 ± 0.0088 | 0.8557 ± 0.0167 |
| log loss | 0.0385 ± 0.0126 | 0.0499 ± 0.0105 | 0.0716 ± 0.0049 |
| Brier skóre | 0.0036 ± 0.0012 | 0.0069 ± 0.0009 | 0.0148 ± 0.0014 |

Rozdiel ROC-AUC train − validácia: **0.0003** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9969 ± 0.0004 | 0.9937 ± 0.0002 | 0.9820 ± 0.0016 |
| balanced accuracy | 0.9967 ± 0.0003 | 0.9931 ± 0.0002 | 0.9829 ± 0.0015 |
| precision | 0.9979 ± 0.0003 | 0.9956 ± 0.0002 | 0.9950 ± 0.0006 |
| recall (TPR) | 0.9975 ± 0.0006 | 0.9949 ± 0.0003 | 0.9717 ± 0.0025 |
| FPR | 0.0041 ± 0.0005 | 0.0086 ± 0.0004 | 0.0058 ± 0.0006 |
| F1 | 0.9977 ± 0.0003 | 0.9953 ± 0.0001 | 0.9832 ± 0.0015 |
| MCC | 0.9932 ± 0.0008 | 0.9859 ± 0.0004 | 0.9641 ± 0.0031 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9968 ± 0.0005 | 0.9933 ± 0.0004 | 0.9820 ± 0.0032 |
| balanced accuracy | 0.9963 ± 0.0007 | 0.9925 ± 0.0006 | 0.9829 ± 0.0028 |
| precision | 0.9974 ± 0.0006 | 0.9949 ± 0.0007 | 0.9942 ± 0.0009 |
| recall (TPR) | 0.9977 ± 0.0003 | 0.9949 ± 0.0001 | 0.9725 ± 0.0066 |
| FPR | 0.0051 ± 0.0012 | 0.0100 ± 0.0013 | 0.0068 ± 0.0011 |
| F1 | 0.9975 ± 0.0004 | 0.9949 ± 0.0003 | 0.9832 ± 0.0030 |
| MCC | 0.9928 ± 0.0011 | 0.9850 ± 0.0009 | 0.9641 ± 0.0061 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 5.1 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 1 364 417 |
| veľkosť modelu na disku | 5.53 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.042 ms |
| transformácia vstupu – priepustnosť | 37 862 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.262 ms (p95 0.291) |
| CPU priepustnosť (24 vlákien) | 51 114 vzoriek/s |
| GPU latencia (batch 1) | 0.710 ms (p95 1.115) |
| GPU priepustnosť | 79 490 vzoriek/s |
| GPU špičková pamäť | 1570 MB |

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
