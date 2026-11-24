# Využívanie príznakov – hybrid

> Generované `src/evaluation/feature_importance.py` (2026-11-23T20:26:53+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| static:permissions | 0.2829 | 0.2710 | 0.2800 | 0.3048 | 0.3297 |
| dynamic:syscalls | 0.0643 | 0.0751 | 0.0415 | 0.0542 | 0.0537 |
| static:metadata | 0.0086 | 0.0120 | 0.0130 | 0.0146 | 0.0110 |
| dynamic:total | 0.0021 | 0.0003 | 0.0000 | 0.0000 | 0.0000 |

## Sledované príznaky (možné artefakty datasetu)
| príznak | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| `general_has_signature` | – | – | – | – | – |
| `datadir_CERTIFICATE_TABLE_size` | – | – | – | – | – |
| `datadir_CERTIFICATE_TABLE_virtual_address` | – | – | – | – | – |
| `header_coff_timestamp` | – | – | – | – | – |
| `strings_urls` | – | – | – | – | – |
| `datadir_RESOURCE_TABLE_size` | – | – | – | – | – |

Interpretácia: pokles blízko 0 = model sa bez príznaku zaobíde (často preto, že rovnakú informáciu nesú iné príznaky).
Permutácia jedného príznaku podhodnocuje skupinu korelovaných príznakov – preto aj kontrolný experiment bez nich
(`runs/comparison/static_ablations/`).
