# Využívanie príznakov – dynamic

> Generované `src/evaluation/feature_importance.py` (2026-11-23T00:18:21+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| syscalls | 0.3945 | 0.4752 | 0.4871 | 0.4816 | 0.4864 |
| total | 0.0053 | 0.0010 | 0.0008 | 0.0138 | 0.0124 |

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
