# Využívanie príznakov – hybrid

> Generované `src/evaluation/feature_importance.py` (2026-11-22T20:28:50+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| static:permissions | 0.2191 | 0.2007 | 0.1985 | 0.2663 | 0.2509 |
| dynamic:syscalls | 0.1339 | 0.1768 | 0.1314 | 0.1130 | 0.1115 |
| static:metadata | 0.0064 | 0.0078 | 0.0091 | 0.0075 | 0.0068 |
| dynamic:total | 0.0000 | 0.0002 | 0.0000 | 0.0002 | 0.0002 |

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
