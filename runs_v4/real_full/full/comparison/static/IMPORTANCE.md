# Využívanie príznakov – static

> Generované `src/evaluation/feature_importance.py` (2026-11-22T19:17:23+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| permissions | 0.3943 | 0.4217 | 0.4183 | 0.4478 | 0.4475 |
| metadata | 0.0217 | 0.0481 | 0.0480 | 0.0358 | 0.0366 |

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
