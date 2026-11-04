# hybrid/mlp_large – beh `20261104-043720`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `mlp` – veľká neurónová sieť (3–5 skrytých vrstiev, 512–2048 neurónov), kandidát na učiteľa
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/mlp_large/20261102-064138`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"max_epochs": 100, "patience": 8, "hidden_layers": 4, "hidden_width": 512, "width_decay": 0.5, "dropout": 0.1951820260605614, "lr": 0.000176468680848935, "weight_decay": 1.209699321025492e-05, "batch_size": 512}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 1.0000 ± 0.0000 | 0.9996 ± 0.0000 | 0.9879 ± 0.0051 |
| PR-AUC | 1.0000 ± 0.0000 | 0.9998 ± 0.0000 | 0.9910 ± 0.0035 |
| TPR pri FPR 1 % | 0.9995 ± 0.0000 | 0.9970 ± 0.0003 | 0.8809 ± 0.0016 |
| TPR pri FPR 0,1 % | 0.9988 ± 0.0002 | 0.9754 ± 0.0090 | 0.8029 ± 0.0064 |
| log loss | 0.0107 ± 0.0019 | 0.0239 ± 0.0022 | 0.3605 ± 0.0121 |
| Brier skóre | 0.0012 ± 0.0001 | 0.0045 ± 0.0002 | 0.0718 ± 0.0018 |

Rozdiel ROC-AUC train − validácia: **0.0004** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9988 ± 0.0002 | 0.9950 ± 0.0003 | 0.9273 ± 0.0029 |
| balanced accuracy | 0.9988 ± 0.0002 | 0.9941 ± 0.0003 | 0.9325 ± 0.0026 |
| precision | 0.9994 ± 0.0003 | 0.9954 ± 0.0001 | 0.9944 ± 0.0008 |
| recall (TPR) | 0.9988 ± 0.0003 | 0.9970 ± 0.0003 | 0.8708 ± 0.0062 |
| FPR | 0.0011 ± 0.0005 | 0.0087 ± 0.0002 | 0.0058 ± 0.0009 |
| F1 | 0.9991 ± 0.0001 | 0.9962 ± 0.0002 | 0.9285 ± 0.0032 |
| MCC | 0.9974 ± 0.0004 | 0.9890 ± 0.0006 | 0.8630 ± 0.0049 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9986 ± 0.0002 | 0.9947 ± 0.0004 | 0.9229 ± 0.0016 |
| balanced accuracy | 0.9988 ± 0.0002 | 0.9942 ± 0.0002 | 0.9285 ± 0.0014 |
| precision | 0.9997 ± 0.0001 | 0.9961 ± 0.0002 | 0.9959 ± 0.0006 |
| recall (TPR) | 0.9980 ± 0.0002 | 0.9959 ± 0.0008 | 0.8612 ± 0.0032 |
| FPR | 0.0005 ± 0.0002 | 0.0074 ± 0.0004 | 0.0042 ± 0.0006 |
| F1 | 0.9989 ± 0.0002 | 0.9960 ± 0.0003 | 0.9237 ± 0.0017 |
| MCC | 0.9969 ± 0.0005 | 0.9884 ± 0.0008 | 0.8557 ± 0.0026 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 6.8 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 2 386 305 |
| veľkosť modelu na disku | 9.67 MB |
| transformácia vstupu – latencia (1 vlákno) | 0.062 ms |
| transformácia vstupu – priepustnosť | 22 120 vzoriek/s |
| CPU latencia modelu (batch 1, 1 vlákno) | 0.295 ms (p95 0.331) |
| CPU priepustnosť (24 vlákien) | 28 807 vzoriek/s |
| GPU latencia (batch 1) | 0.509 ms (p95 1.079) |
| GPU priepustnosť | 31 491 vzoriek/s |
| GPU špičková pamäť | 2800 MB |

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
