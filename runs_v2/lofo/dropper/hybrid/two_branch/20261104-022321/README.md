# hybrid_seq/two_branch – beh `20261104-022321`

> Automaticky generované (`src/training/run_tabular.py`). Konfigurácia: `config.yaml`, protokol: `protocol.yaml`.

- **Model:** `two_branch` – statická MLP vetva + sekvenčná CNN vetva nad API volaniami, spojené v spoločnej hlave
- **Ladenie:** bez ladenia – hyperparametre prevzaté z `runs_final/hybrid/two_branch/20261102-170657`
- **Finálne modely:** seedy [0, 1, 2]; hodnoty sú priemer ± smerodajná odchýlka cez seedy
- **Najlepšie hyperparametre:** `{"n_static": 2381, "width_decay": 0.5, "max_epochs": 30, "patience": 4, "static_layers": 3, "static_width": 256, "emb_dim": 64, "channels": 256, "kernels": "2-4-8", "hidden": 512, "dropout": 0.32477392485404594, "lr": 0.0006728393356648638, "weight_decay": 0.0003230215070317658, "batch_size": 256}`

## Detekčná kvalita (bez prahu)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| ROC-AUC | 0.9999 ± 0.0001 | 0.9992 ± 0.0001 | 0.9985 ± 0.0001 |
| PR-AUC | 0.9999 ± 0.0000 | 0.9996 ± 0.0001 | 0.9988 ± 0.0002 |
| TPR pri FPR 1 % | 0.9994 ± 0.0004 | 0.9958 ± 0.0005 | 0.9841 ± 0.0072 |
| TPR pri FPR 0,1 % | 0.9853 ± 0.0065 | 0.9350 ± 0.0184 | 0.8298 ± 0.0292 |
| log loss | 0.0104 ± 0.0036 | 0.0287 ± 0.0011 | 0.0674 ± 0.0089 |
| Brier skóre | 0.0027 ± 0.0008 | 0.0058 ± 0.0006 | 0.0158 ± 0.0024 |

Rozdiel ROC-AUC train − validácia: **0.0007** (veľký rozdiel = preučenie).

## Pri prahu z validácie (FPR ≤ 1% na validácii)
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9969 ± 0.0006 | 0.9938 ± 0.0003 | 0.9837 ± 0.0050 |
| balanced accuracy | 0.9965 ± 0.0004 | 0.9931 ± 0.0003 | 0.9844 ± 0.0048 |
| precision | 0.9968 ± 0.0003 | 0.9944 ± 0.0001 | 0.9938 ± 0.0019 |
| recall (TPR) | 0.9983 ± 0.0012 | 0.9958 ± 0.0005 | 0.9760 ± 0.0082 |
| FPR | 0.0053 ± 0.0005 | 0.0096 ± 0.0002 | 0.0073 ± 0.0022 |
| F1 | 0.9975 ± 0.0005 | 0.9951 ± 0.0003 | 0.9848 ± 0.0047 |
| MCC | 0.9935 ± 0.0012 | 0.9868 ± 0.0008 | 0.9674 ± 0.0100 |

## Pri pevnom prahu 0.5
| metrika | train (podvzorka) | validácia | test |
|---|---|---|---|
| accuracy | 0.9959 ± 0.0019 | 0.9927 ± 0.0021 | 0.9793 ± 0.0027 |
| balanced accuracy | 0.9960 ± 0.0014 | 0.9924 ± 0.0019 | 0.9804 ± 0.0027 |
| precision | 0.9976 ± 0.0007 | 0.9950 ± 0.0006 | 0.9951 ± 0.0020 |
| recall (TPR) | 0.9958 ± 0.0036 | 0.9933 ± 0.0028 | 0.9665 ± 0.0031 |
| FPR | 0.0039 ± 0.0011 | 0.0085 ± 0.0010 | 0.0056 ± 0.0022 |
| F1 | 0.9967 ± 0.0016 | 0.9942 ± 0.0017 | 0.9806 ± 0.0026 |
| MCC | 0.9914 ± 0.0040 | 0.9843 ± 0.0045 | 0.9588 ± 0.0054 |

## Výpočtové nároky (seed 0, testovacia množina)
| meranie | hodnota |
|---|---|
| tréning finálneho modelu | 462.9 s (priemer cez seedy) |
| ladenie spolu | 0 s |
| počet parametrov / uzlov | 1 756 866 |
| veľkosť modelu na disku | 7.10 MB |
| CPU latencia modelu (batch 1, 1 vlákno) | 5.100 ms (p95 5.713) |
| CPU priepustnosť (24 vlákien) | 657 vzoriek/s |
| GPU latencia (batch 1) | 1.311 ms (p95 2.769) |
| GPU priepustnosť | 4 412 vzoriek/s |
| GPU špičková pamäť | 3758 MB |

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
